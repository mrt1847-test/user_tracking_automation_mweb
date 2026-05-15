import json
import logging
import time
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import Page, Request


logger = logging.getLogger(__name__)


class MontelenaTracker:
    """
    Collects POST requests sent to montelena-rcv.gmarket.co.kr/montelena/add.

    This tracker is intentionally separate from NetworkTracker so the existing
    aplus.gmarket.co.kr collection and validation flow stays unchanged.
    """

    ENDPOINT_HOST = "montelena-rcv.gmarket.co.kr"
    ENDPOINT_PATH = "/montelena/add"

    def __init__(self, page: Page):
        self.page = page
        self.context = page.context
        self.tracked_pages: List[Page] = [page]
        self.logs: List[Dict[str, Any]] = []
        self.is_tracking = False

    def _is_target_request(self, url: str) -> bool:
        parsed = urlparse(url)
        return (
            parsed.netloc.lower() == self.ENDPOINT_HOST
            and parsed.path == self.ENDPOINT_PATH
        )

    def _parse_payload(self, post_data: Optional[str]) -> Any:
        if not post_data:
            return {}

        try:
            return json.loads(post_data)
        except (json.JSONDecodeError, TypeError):
            pass

        try:
            parsed_form = parse_qs(post_data, keep_blank_values=True)
            if not parsed_form:
                return post_data

            normalized: Dict[str, Any] = {}
            for key, values in parsed_form.items():
                value: Any = values[0] if len(values) == 1 else values
                if isinstance(value, str):
                    try:
                        value = json.loads(value)
                    except json.JSONDecodeError:
                        pass
                normalized[key] = value
            return normalized
        except Exception as exc:
            logger.debug("Montelena payload parse failed: %s", exc)
            return post_data

    def _classify_event_type(self, payload: Any) -> str:
        if isinstance(payload, dict):
            event_type = payload.get("type")
            if event_type is not None and str(event_type).strip():
                return str(event_type)
        return "Unknown"

    def _on_request(self, request: Request):
        if not self.is_tracking:
            return

        try:
            url = request.url if isinstance(request.url, str) else request.url()
            method = request.method if isinstance(request.method, str) else request.method()

            if method.upper() != "POST" or not self._is_target_request(url):
                return

            post_data = (
                request.post_data()
                if callable(getattr(request, "post_data", None))
                else getattr(request, "post_data", None)
            )
            payload = self._parse_payload(post_data)
            event_type = self._classify_event_type(payload)

            log_entry = {
                "type": event_type,
                "event_type": event_type,
                "url": url,
                "payload": payload,
                "timestamp": time.time(),
                "method": method,
                "endpoint": "montelena",
            }
            self.logs.append(log_entry)
            logger.info("Montelena %s event captured: %s", event_type, url)
        except Exception as exc:
            logger.error("Montelena request handling failed: %s", exc, exc_info=True)

    def start(self):
        if self.is_tracking:
            logger.warning("Montelena tracking is already started.")
            return

        self.is_tracking = True
        self.context.on("request", self._on_request)
        self.context.on("page", self._on_new_page)

        for page in self.context.pages:
            if page not in self.tracked_pages:
                self.tracked_pages.append(page)

        logger.info("Montelena tracking started (pages: %s)", len(self.tracked_pages))

    def _on_new_page(self, page: Page):
        if not self.is_tracking:
            return

        if page not in self.tracked_pages:
            self.tracked_pages.append(page)
            logger.info("Montelena tracking added new page: %s", page.url or "loading")

    def stop(self):
        if not self.is_tracking:
            logger.warning("Montelena tracking is not started.")
            return

        self.is_tracking = False
        try:
            self.context.off("request", self._on_request)
            self.context.off("page", self._on_new_page)
        except Exception as exc:
            logger.warning("Montelena listener removal failed and was ignored: %s", exc)

        logger.info("Montelena tracking stopped")

    def get_logs(self, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        if event_type:
            return [
                log
                for log in self.logs
                if self._event_type_matches(str(log.get("type", "")), event_type)
            ]
        return self.logs.copy()

    def get_logs_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        return self.get_logs(event_type)

    def _event_type_matches(self, actual: str, expected: str) -> bool:
        actual_normalized = actual.strip().lower()
        expected_normalized = expected.strip().lower()
        if expected_normalized in ("pageview", "pageviwe"):
            return actual_normalized == "pageview"
        return actual == expected

    def get_click_logs(self) -> List[Dict[str, Any]]:
        return self.get_logs("click")

    def get_pageview_logs(self) -> List[Dict[str, Any]]:
        return self.get_logs("pageView")

    def get_imp_logs(self) -> List[Dict[str, Any]]:
        return [log for log in self.logs if str(log.get("type", "")).lower().startswith("imp")]

    def get_logs_by_areacode(self, areacode: str, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        logs = self.get_logs(event_type)
        return [
            log
            for log in logs
            if isinstance(log.get("payload"), dict)
            and str(log["payload"].get("areacode")) == str(areacode)
        ]

    def get_logs_by_goodscode(self, goodscode: str, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        logs = self.get_logs(event_type)
        return [
            log
            for log in logs
            if str(self.find_value(log.get("payload"), "GOODSCODE")) == str(goodscode)
            or str(self.find_value(log.get("payload"), "goodscode")) == str(goodscode)
            or str(self.find_value(log.get("payload"), "x_object_id")) == str(goodscode)
        ]

    def find_value(self, obj: Any, target_key: str, visited: Optional[set] = None) -> Optional[Any]:
        if visited is None:
            visited = set()

        if isinstance(obj, (dict, list)):
            obj_id = id(obj)
            if obj_id in visited:
                return None
            visited.add(obj_id)

        try:
            if isinstance(obj, dict):
                if target_key in obj:
                    return obj[target_key]

                target_key_lower = target_key.lower()
                for key, value in obj.items():
                    if isinstance(key, str) and key.lower() == target_key_lower:
                        return value

                for value in obj.values():
                    if isinstance(value, str) and value.strip().startswith(("{", "[")):
                        try:
                            parsed_value = json.loads(value)
                            found = self.find_value(parsed_value, target_key, visited)
                            if found is not None:
                                return found
                        except json.JSONDecodeError:
                            pass

                    if isinstance(value, str):
                        parsed_query = self._parse_url_query(value)
                        if parsed_query:
                            found = self.find_value(parsed_query, target_key, visited)
                            if found is not None:
                                return found

                    found = self.find_value(value, target_key, visited)
                    if found is not None:
                        return found

            if isinstance(obj, list):
                for item in obj:
                    found = self.find_value(item, target_key, visited)
                    if found is not None:
                        return found
        finally:
            if isinstance(obj, (dict, list)):
                visited.discard(id(obj))

        return None

    def _parse_url_query(self, value: str) -> Dict[str, Any]:
        if not value or "?" not in value:
            return {}

        parsed_url = urlparse(value)
        if not parsed_url.query:
            return {}

        parsed_query = parse_qs(parsed_url.query, keep_blank_values=True)
        normalized: Dict[str, Any] = {}
        for key, values in parsed_query.items():
            normalized_value: Any = values[0] if len(values) == 1 else values
            if isinstance(normalized_value, str):
                try:
                    normalized_value = json.loads(normalized_value)
                except json.JSONDecodeError:
                    pass
            normalized[key] = normalized_value

        return normalized

    def validate_payload(
        self,
        log: Dict[str, Any],
        expected_data: Dict[str, Any],
    ) -> Tuple[bool, Dict[str, Dict[str, Any]]]:
        payload = log.get("payload")
        if not isinstance(payload, dict):
            raise AssertionError(
                f"Montelena payload is not a dictionary. URL: {log.get('url')}, payload: {payload}"
            )

        errors: List[str] = []
        passed_fields: Dict[str, Dict[str, Any]] = {}

        for key, expected_value in expected_data.items():
            if expected_value in ("skip", "__SKIP__"):
                passed_fields[key] = {"expected": expected_value, "actual": "(skip)"}
                continue

            actual_value = self.find_value(payload, key)

            if expected_value in ("mandatory", "__MANDATORY__"):
                if actual_value is None or (isinstance(actual_value, str) and not actual_value.strip()):
                    errors.append(f"'{key}' is mandatory but empty or missing.")
                else:
                    passed_fields[key] = {"expected": expected_value, "actual": actual_value}
                continue

            if actual_value is None:
                errors.append(f"'{key}' value was not found.")
                continue

            if str(actual_value) != str(expected_value):
                errors.append(
                    f"'{key}' mismatch. expected: {expected_value}, actual: {actual_value}"
                )
                continue

            passed_fields[key] = {"expected": expected_value, "actual": actual_value}

        if errors:
            raise AssertionError(
                "Montelena payload validation failed:\n"
                + "\n".join(errors)
                + "\nPayload: "
                + json.dumps(payload, ensure_ascii=False, indent=2)
            )

        return True, passed_fields

    def clear_logs(self):
        self.logs.clear()
        logger.info("Montelena logs cleared")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
