"""
BDD Step Definitions for Network Tracking
네트워크 트래킹 관련 공통 스텝 정의
"""
import time
import logging
from pytest_bdd import given, when
from utils.NetworkTracker import NetworkTracker
from utils.MontelenaTracker import MontelenaTracker

logger = logging.getLogger(__name__)


@given("네트워크 트래킹이 시작되었음")
def given_network_tracking_started(page, bdd_context):
    """네트워크 트래킹 시작"""
    logger.info("네트워크 트래킹 시작")
    tracker = NetworkTracker(page)
    tracker.start()
    bdd_context['tracker'] = tracker


@given("몬텔레나 트래킹이 시작되었음")
def given_montelena_tracking_started(page, bdd_context):
    """Montelena 트래킹 시작"""
    logger.info("Montelena 트래킹 시작")
    tracker = MontelenaTracker(page)
    tracker.start()
    bdd_context['montelena_tracker'] = tracker


@given("네트워크 및 몬텔레나 트래킹이 시작되었음")
def given_network_and_montelena_tracking_started(page, bdd_context):
    """기존 aplus 트래킹과 Montelena 트래킹을 함께 시작"""
    logger.info("네트워크 및 Montelena 트래킹 시작")

    network_tracker = NetworkTracker(page)
    network_tracker.start()
    bdd_context['tracker'] = network_tracker

    montelena_tracker = MontelenaTracker(page)
    montelena_tracker.start()
    bdd_context['montelena_tracker'] = montelena_tracker


@when("네트워크 요청이 완료될 때까지 대기함")
def when_wait_for_network_request_completion():
    """네트워크 요청 완료 대기"""
    logger.info("네트워크 요청 완료 대기")
    time.sleep(2)


@when("네트워크 트래킹을 중지함")
def when_stop_network_tracking(bdd_context):
    """네트워크 트래킹 중지"""
    logger.info("네트워크 트래킹 중지")
    tracker = bdd_context.get('tracker')
    if tracker:
        tracker.stop()
    else:
        logger.warning("트래킹이 시작되지 않았습니다.")

    montelena_tracker = bdd_context.get('montelena_tracker')
    if montelena_tracker:
        montelena_tracker.stop()
