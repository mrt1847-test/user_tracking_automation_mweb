Feature: G마켓 PDP 트래킹 로그 정합성 검증
  상품 상세 페이지에서 상품 클릭 시 트래킹 로그의 정합성을 검증합니다.
  
  Scenario: 상품 상세 페이지에서 모듈별 상품 클릭 시 트래킹 로그 검증
    Given G마켓 홈 페이지에 접속했음
    And 네트워크 트래킹이 시작되었음
    And 상품 "<goodscode>"의 상세페이지로 접속했음
    When 사용자가 PDP에서 "<module_title>" 모듈 내 상품을 확인하고 클릭한다
    Then 상품 페이지로 이동되었다
    Then Module Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_module_exposure>)
    And Product Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_exposure>)
    And Product Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_click>)
        
    Examples:
      | goodscode  | module_title                | tc_module_exposure | tc_product_exposure | tc_product_click |
      | 2522715372 | 이마트몰VT                   | C1228951           | C1228952            | C1228954         |
      | 2522715372 | 이마트몰BT                   | C1166910           | C1166911            | C1166913         |
      | 2522715372 | 이 브랜드의 인기상품          | C1166914           | C1166915            | C1166917         |
      | 2522715372 | 점포 행사 상품이에요          | C1166918           | C1166919            | C1166921         | 
      | 4457587710 | BuyBox                      | C1228940           | C1228941            | C1228943         |
      
  