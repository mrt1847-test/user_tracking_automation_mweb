"""
G마켓 홈 페이지 객체
"""
from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.urls import base_url
import logging

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """G마켓 홈 페이지"""
    
    # 선택자 정의
    SEARCH_INPUT = "input[placeholder*='검색']"
    SEARCH_BUTTON = "button[type='submit']"
    LOGIN_BUTTON = "로그인"
    LOGOUT_BUTTON = "text=로그아웃"
    
    def __init__(self, page: Page):
        """
        HomePage 초기화
        
        Args:
            page: Playwright Page 객체
        """
        super().__init__(page)
        self.base_url = base_url()
    
    def navigate(self) -> None:
        """홈 페이지로 이동"""
        logger.info("홈 페이지로 이동")
        self.goto(self.base_url)
    
    def fill_search_input(self, keyword: str) -> None:
        """
        검색어 입력
        
        Args:
            keyword: 검색할 상품명
        """
        logger.debug(f"검색어 입력: {keyword}")
        self.page.fill("input[name='keyword']", keyword)
    
    def click_search_button(self) -> None:
        """검색 버튼 클릭 (fieldset 내 검색 버튼)"""
        logger.debug("검색 버튼 클릭")
        self.page.locator("fieldset").get_by_role("button", name="검색", exact=True).click()
        logger.info("검색 버튼 클릭 완료")
    
    def search_product(self, keyword: str) -> None:
        """
        홈화면에서 특정 keyword로 검색
        검색 버튼 클릭 → 검색어 입력 → 검색 실행
        
        Args:
            keyword: 검색어
        """
        runtext = f"Home > {keyword} 검색"
        logger.info("%s 시작", runtext)
        self.page.get_by_role("button", name="검색").click()
        self.page.fill("input[name='keyword']", keyword)
        self.page.locator("fieldset").get_by_role("button", name="검색", exact=True).click()
        logger.info("%s 종료", runtext)
    
    def wait_for_search_results(self) -> None:
        """검색 결과 페이지 로드 대기"""
        logger.debug("검색 결과 로드 대기")
        self.page.wait_for_load_state("networkidle")
    
    def click_login(self) -> None:
        """로그인 버튼 클릭"""
        logger.info("로그인 버튼 클릭")
        login_button = self.page.get_by_text("로그인", exact=True)
        
        # 요소가 실제로 존재하는지 확인
        count = login_button.count()
        if count == 0:
            raise Exception("로그인 버튼을 찾을 수 없습니다")
        logger.debug(f"로그인 버튼 {count}개 발견")
        
        # 요소가 클릭 가능한 상태가 될 때까지 대기
        login_button.wait_for(state="visible", timeout=10000)
        login_button.scroll_into_view_if_needed()
        
        # 요소가 실제로 클릭 가능한지 확인
        is_visible = login_button.is_visible()
        is_enabled = login_button.is_enabled() if hasattr(login_button, 'is_enabled') else True
        logger.debug(f"로그인 버튼 상태 - visible: {is_visible}, enabled: {is_enabled}")
        
        if not is_visible:
            raise Exception("로그인 버튼이 보이지 않습니다")
        
        # 현재 URL 저장 (클릭 전)
        current_url = self.page.url
        logger.debug(f"클릭 전 URL: {current_url}")
        
        # 클릭 시도
        try:
            login_button.click(timeout=5000)
            logger.debug("일반 클릭 성공")
        except Exception as e:
            logger.warning(f"일반 클릭 실패, force 클릭 시도: {e}")
            login_button.click(force=True)
            logger.debug("force 클릭 완료")
        
        # 클릭 후 로그인 페이지로 이동했는지 확인
        try:
            # 로그인 페이지의 입력 필드가 나타날 때까지 대기
            self.page.wait_for_selector("#typeMemberInputId", timeout=5000)
            logger.info("로그인 페이지로 이동 확인됨")
        except Exception as e:
            # URL이 변경되었는지 확인
            new_url = self.page.url
            logger.warning(f"로그인 페이지 요소를 찾을 수 없음. 현재 URL: {new_url}")
            if current_url == new_url:
                raise Exception(f"로그인 버튼 클릭 후 페이지가 변경되지 않았습니다. URL: {new_url}")
        
        logger.info("로그인 버튼 클릭 완료")
    
    def is_logged_in(self) -> bool:
        """
        로그인 상태 확인
        
        Returns:
            로그인되어 있으면 True, 아니면 False
        """
        return self.is_visible("text='로그아웃'", timeout=5000)
    
    def click_logout(self) -> None:
        """로그아웃 버튼 클릭"""
        logger.info("로그아웃 버튼 클릭")
        self.click("text='로그아웃'")

    def click_cart(self) -> None:
        """장바구니 버튼 클릭"""
        logger.info("장바구니 버튼 클릭")
        self.click("[title='장바구니']")

    def click_my_page(self) -> None:
        """마이페이지 버튼 클릭"""
        logger.info("마이페이지 버튼 클릭")
        self.click(".link__myg")

    def click_rvh(self) -> None:
        """RVH 버튼 클릭"""
        logger.info("RVH 버튼 클릭")
        self.click(".link__rvh")

    def wait_for_rvh_page_load(self, timeout: int = None) -> bool:
        """
        RVH 페이지 로드 대기.
        span.desc-txt "쇼핑 히스토리예요." 요소가 보일 때까지 대기한 뒤 표시 여부를 반환한다.

        Args:
            timeout: 타임아웃(ms). None이면 self.timeout 사용.

        Returns:
            요소가 보이면 True, 타임아웃 등으로 실패하면 False.
        """
        timeout = timeout or self.timeout
        logger.debug("RVH 페이지 로드 대기 (span.desc-txt '쇼핑 히스토리예요.')")
        try:
            loc = self.page.locator("span.desc-txt", has_text="쇼핑 히스토리예요.")
            loc.wait_for(state="visible", timeout=timeout)
            visible = loc.is_visible()
            if visible:
                logger.info("RVH 페이지 로드 확인됨")
            return visible
        except Exception as e:
            logger.warning("RVH 페이지 로드 대기 실패: %s", e)
            return False

    def is_recently_viewed_displayed(self, timeout: int = None) -> bool:
        """
        최근 본 내역이 노출되는지 확인.
        strong.list-rvh__date (날짜 헤딩, 예: 2026.02.24 오늘) 요소가 보이면 True.

        Args:
            timeout: 타임아웃(ms). None이면 self.timeout 사용.

        Returns:
            노출되어 있으면 True, 아니면 False.
        """
        timeout = timeout or self.timeout
        logger.debug("최근 본 내역 노출 확인 (strong.list-rvh__date)")
        try:
            loc = self.page.locator("strong.list-rvh__date").first
            loc.wait_for(state="visible", timeout=timeout)
            visible = loc.is_visible()
            if visible:
                logger.info("최근 본 내역 노출 확인됨")
            return visible
        except Exception as e:
            logger.warning("최근 본 내역 노출 확인 실패: %s", e)
            return False

    def get_product_in_module(self):
        """
        모듈 내 상품 요소 찾기
        """
        logger.debug("모듈 내 상품 요소 찾기")
        return self.page.locator(".list-rvh__content-item--product a").first
