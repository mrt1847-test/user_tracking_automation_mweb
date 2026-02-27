Feature: G마켓 PDP 트래킹 로그 정합성 검증
  상품 상세 페이지에서 상품 클릭 시 트래킹 로그의 정합성을 검증합니다.
  
  Scenario: 그룹 연관상품 상세보기 페이지에서 연관 상품 클릭 시 트래킹 로그 검증
    Given G마켓 홈 페이지에 접속했음
    And 네트워크 트래킹이 시작되었음
    And 상품 "<goodscode>"의 상세페이지로 접속했음
    When 사용자가 PDP에서 "<location_title>"을 클릭한다
    And 사용자가 PDP에서 "<module_title>" 모듈 내 상품을 확인하고 클릭한다
    Then 레이어 "연관상품 상세보기"가 출력되었다
    Then 모든 트래킹 로그를 JSON 파일로 저장함
    Then Module Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_module_exposure>)
    And Product Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_exposure>)
    And Product Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_click>)
    
    Examples:
      | goodscode  | location_title     | module_title     | tc_module_exposure | tc_product_exposure | tc_product_click |
      | 3039555146 | 연관상품            | 연관상품 상세보기 |                    | C1228983            | C1228984         |