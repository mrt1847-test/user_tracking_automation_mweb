Feature: G마켓 PDP 트래킹 로그 정합성 검증
  상품 상세 페이지에서 상품 클릭 시 트래킹 로그의 정합성을 검증합니다.
  
  Scenario: 상품 상세 페이지에서 버튼 클릭 시 트래킹 로그 검증
    Given G마켓 홈 페이지에 접속했음
    And 네트워크 트래킹이 시작되었음
    And 상품 "<goodscode>"의 상세페이지로 접속했음
    When 사용자가 PDP에서 "<location_title>"을 클릭한다
    And 사용자가 상품 옵션을 입력한다
    And 사용자가 PDP에서 "<module_title>" 버튼을 확인하고 클릭한다
    Then 버튼 "<module_title>"가 클릭되었다
    And PDP Buynow Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_buynow_click>)
    And PDP ATC Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_atc_click>)
    And PDP Gift Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_gift_click>)
    And PDP Rental Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_rental_click>)
    And PDP Join Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_join_click>)
    
    Examples:
      | goodscode  | location_title | module_title     | tc_buynow_click | tc_atc_click | tc_gift_click | tc_rental_click | tc_join_click |
      | 4448231882 | 구매하기        | 일반상품 구매하기 | C1166905        |              |               |                 |               |      
      | 4448231882 | 구매하기        | 일반상품 장바구니 |                 | C1166904     |               |                 |               |
      | 4448231882 | 선물하기        | 일반상품 선물하기 |                 |              | C1166903      |                 |               |
      | 2698619898 | 상담 신청하기   | 상담신청          |                 |              |               | C1166931        |               |
      | 2529094051 | 가입 신청하기   | 가입신청          |                 |              |               |                 | C1166932      |