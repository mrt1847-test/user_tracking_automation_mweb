Feature: G마켓 PDP 트래킹 로그 정합성 검증
  상품 상세 페이지에서 상품 클릭 시 트래킹 로그의 정합성을 검증합니다.
  
  Scenario: 그룹 상품 상세 페이지에서 버튼 클릭 시 트래킹 로그 검증
    Given G마켓 홈 페이지에 접속했음
    And 네트워크 트래킹이 시작되었음
    And 상품 "4457587710"의 상세페이지로 접속했음
    When 사용자가 PDP에서 "가격 비교하기"을 클릭한다
    And 사용자가 BuyBox에서 "낮은가격순" 모듈 내 상품을 확인하고 클릭한다
    Then 상품 페이지로 이동되었다
    Then Module Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_module_exposure>)
    And Product Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_exposure>)
    And Product Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_click>)