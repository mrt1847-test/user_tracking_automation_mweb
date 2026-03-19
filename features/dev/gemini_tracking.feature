Feature: G마켓 SRP 트래킹 로그 정합성 검증
  검색 결과 페이지에서 상품 클릭 시 트래킹 로그의 정합성을 검증합니다.

  Scenario: 검색 결과 페이지에서 모듈별 상품 클릭 시 트래킹 로그 검증
    Given G마켓 홈 페이지에 접속했음
    And 네트워크 트래킹이 시작되었음
    When 사용자가 "<keyword>"을 검색한다
    Then 검색 결과 페이지가 표시된다
    Given 사용자가 "<keyword>"을 검색했다
    And 검색 결과 페이지에 "<module_title>" 모듈이 있다
    When 사용자가 "<module_title>" 모듈 내 1번째 상품을 확인하고 클릭한다
    Then 상품 페이지로 이동되었다
    Then 모든 트래킹 로그를 JSON 파일로 저장함
    Then Module Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_module_exposure>)
    And Product Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_exposure>)
    And Product Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_click>)
    And Product ATC Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_atc_click>)

    Examples:
      | keyword          | module_title      | tc_module_exposure | tc_product_exposure | tc_product_click | tc_atc_click   |
      | 물티슈            | 카탈로그 속성형     | C1228806           | C1228807            | C1228811         | C1228812       |
      | 물티슈            | 카탈로그 그룹형     | C1228846           | C1228847            | C1228849         | C1228850       |
      | 물티슈            | 카탈로그 일반형     | C1228902           | C1228903            | C1228905         | C1228906       |

  Scenario: 검색 결과 페이지에서 카탈로그 모듈 더보기기 상품 클릭 시 트래킹 로그 검증
    Given G마켓 홈 페이지에 접속했음
    And 네트워크 트래킹이 시작되었음
    When 사용자가 "<keyword>"을 검색한다
    Then 검색 결과 페이지가 표시된다
    Given 사용자가 "<keyword>"을 검색했다
    And 검색 결과 페이지에 "<module_title>" 모듈이 있다
    And 더보기 버튼을 클릭한다
    When 사용자가 "<module_title>" 모듈 내 6번째 상품을 확인하고 클릭한다
    Then 상품 페이지로 이동되었다
    Then 모든 트래킹 로그를 JSON 파일로 저장함
    Then Module Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_module_exposure>)
    And Product Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_exposure>)
    And Product Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_click>)
    And Product ATC Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_atc_click>)

    Examples:
      | keyword          | module_title      | tc_module_exposure | tc_product_exposure | tc_product_click | tc_atc_click   |
      | 물티슈            | 카탈로그 속성형     | C1228806           | C1228807            | C1228811         | C1228812       |
      | 물티슈            | 카탈로그 그룹형     | C1228846           | C1228847            | C1228849         | C1228850       |
      | 물티슈            | 카탈로그 일반형     | C1228902           | C1228903            | C1228905         | C1228906       |

  Scenario: 검색 결과 페이지에서 정렬후후 상품 클릭 시 트래킹 로그 검증
    Given G마켓 홈 페이지에 접속했음
    And 네트워크 트래킹이 시작되었음
    When 사용자가 "<keyword>"을 검색한다
    Then 검색 결과 페이지가 표시된다
    Given 사용자가 "<keyword>"을 검색했다
    When 검색 결과 페이지에서서 "<module_title>" 정렬을 선택한다
    When 사용자가 "<module_title>" 모듈 내 1번째 상품을 확인하고 클릭한다
    Then 상품 페이지로 이동되었다
    Then 모든 트래킹 로그를 JSON 파일로 저장함
    Then Module Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_module_exposure>)
    And Product Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_exposure>)
    And Product Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_click>)
    And Product ATC Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_atc_click>)

    Examples:
      | keyword          | module_title      | tc_module_exposure | tc_product_exposure | tc_product_click | tc_atc_click   |
      | 물티슈            | 판매 인기순     | C1228806           | C1228807            | C1228811         | C1228812       |
      | 물티슈            | 상품평 많은순     | C1228846           | C1228847            | C1228849         | C1228850       |
      | 물티슈            | 신규 상품순     | C1228902           | C1228903            | C1228905         | C1228906       |

     