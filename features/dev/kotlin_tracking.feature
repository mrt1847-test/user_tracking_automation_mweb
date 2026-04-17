Feature: G마켓 Home 트래킹 로그 정합성 검증
  검색 결과 페이지에서 상품 클릭 시 트래킹 로그의 정합성을 검증합니다.

  Scenario: 홈 섹션 모듈별 상품 클릭 시 트래킹 로그 검증
    Given 네트워크 트래킹이 시작되었음
    Given G마켓 홈 페이지에 접속했음
    When 사용자가 "<section_name>" 섹션으로 이동한다
    Then "<section_name>" 섹션으로 이동했다
    Given 섹션에 "<n>"번째 "<module_title>" 모듈이 있다
    When 홈에서 사용자가 "<n>"번째 "<module_title>" 모듈 내 <nth>번째 상품을 확인하고 클릭한다
    Then 상품 페이지로 이동되었다
    Then 모든 트래킹 로그를 JSON 파일로 저장함
    Then Module Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_module_exposure>)
    And Product Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_exposure>)
    And Product Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_click>)

    Examples:
      | section_name  | n | module_title        | nth | tc_module_exposure | tc_product_exposure | tc_product_click | 
      | 홈            | 1 | today_itemcarousel  | 1 | C1413652           | C1413653            | C1413654         | 
      | 홈            | 1 | today_newlowest     | 1 | C1413645           | C1413646            | C1413647         | 
      | 홈            | 1 | today_livedeal      | 1 | C1413606           | C1413607            | C1413608         | 
      | 홈            | 1 | today_shortsdeal    | 1 | C1413652           | C1413653            | C1413654         | 
      | 홈            | 1 | today_branddeal     | 1 | C1413645           | C1413646            | C1413647         | 
      | 홈            | 1 | today_hmjfy0        | 1 | C1413606           | C1413607            | C1413608         | 

  
  