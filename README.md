# User Tracking Automation

G마켓 웹사이트의 사용자 트래킹 로그를 자동으로 수집하고 정합성을 검증하는 **BDD(Behavior-Driven Development) 기반 테스트 자동화 프로젝트**입니다.

## 📋 목차

- [주요 기능](#-주요-기능)
- [프로젝트 구조](#-프로젝트-구조)
- [설치 및 실행](#-설치-및-실행)
- [설정 파일](#️-설정-파일)
- [주요 컴포넌트](#-주요-컴포넌트)
- [사용 방법](#-사용-방법)
- [TestRail 연동](#-testrail-연동)
- [Google Sheets 데이터 관리](#-google-sheets-데이터-관리)
- [문제 해결](#-문제-해결)

## 🎯 주요 기능

1. **BDD 기반 테스트 시나리오 작성**
   - `pytest-bdd`를 사용한 Gherkin 문법 기반 시나리오 작성
   - Feature 파일을 통한 비즈니스 로직 중심 테스트 정의
   - 재사용 가능한 Step Definitions

2. **네트워크 트래킹 로그 수집**
   - `aplus.gmarket.co.kr` 도메인의 POST 요청을 실시간으로 감지
   - 이벤트 타입별 자동 분류 (PV, Module Exposure, Product Exposure, Product Click, PDP PV, Product ATC Click 등)
   - SPM(Search Parameter Map) 기반 필터링
   - 다중 페이지/탭 지원

3. **트래킹 로그 정합성 검증**
   - HTML에서 추출한 가격 정보와 트래킹 로그의 가격 정보 비교
   - 영역별 설정 파일 기반 자동 검증
   - 이벤트 타입별 필드 검증
   - 특수 값 처리 (mandatory, skip, 리스트 값 등)

4. **TestRail 연동**
   - 테스트 실행 시 자동으로 TestRail Run 생성
   - 각 스텝 실행 결과를 TestRail에 자동 기록
   - 실패 시 스크린샷 자동 첨부
   - 실행 로그 자동 수집 및 첨부
   - 프론트엔드 실패 처리 및 Soft Assertion 지원

5. **Google Sheets를 통한 데이터 관리**
   - tracking_all JSON 파일을 Google Sheets로 변환
   - Google Sheets에서 설정 파일 편집 후 JSON으로 변환
   - 영역별 설정 파일 관리 (SRP, LP, CART, MY, ORDER)
   - 관련 스크립트: `scripts/json_to_sheets.py`, `scripts/sheets_to_json.py`

## 📁 프로젝트 구조

```
user_tracking_automation_mweb/
├── tracking_schemas/                 # 트래킹 이벤트 검증용 스키마(JSON)
│   ├── SRP/                          # 검색 결과(SRP) 모듈
│   ├── LP/                           # 리스트/랜딩(LP) 모듈
│   ├── PDP/                          # 상품 상세(PDP) 모듈
│   ├── JFY/                          # JFY(이런 상품은 어때요) 모듈
│   ├── HOME/                         # 홈 모듈
│   ├── CART/                         # 장바구니 영역
│   ├── MY/                           # MY 영역
│   └── ORDER/                        # 주문완료 영역
├── features/                         # BDD feature 파일 (환경별 분리)
│   ├── dev/                          # 개발 환경 시나리오
│   │   └── pdpjfy_tracking.feature
│   └── prod/                         # 운영 환경 시나리오
│       ├── srp_tracking.feature
│       ├── srp_tracking2.feature
│       ├── lp_tracking.feature
│       ├── pdp_tracking.feature
│       ├── pdp_tracking2.feature
│       ├── cart_tracking.feature
│       ├── my_tracking.feature
│       ├── order_complete_tracking.feature
│       ├── rvh_tracking.feature
│       └── ...
├── test/                             # pytest feature 로더 (환경별)
│   ├── dev/                          # dev feature 실행 엔트리
│   │   ├── test_jfy.py
│   │   ├── test_kotlin.py
│   │   └── test_gemini.py
│   └── prod/
│       ├── test_srp.py
│       ├── test_lp.py
│       ├── test_pdp.py
│       ├── test_cart.py
│       ├── test_my.py
│       ├── test_order.py
│       ├── test_home.py
│       └── ...
├── steps/                            # BDD step definitions
│   ├── srp_lp_steps.py
│   ├── product_steps.py
│   ├── cart_steps.py
│   ├── checkout_steps.py
│   ├── order_steps.py
│   ├── my_steps.py
│   ├── home_steps.py
│   ├── tracking_steps.py
│   ├── tracking_validation_steps.py
│   └── login_steps.py
├── pages/                            # Playwright Page Object Model
│   ├── base_page.py
│   ├── search_page.py
│   ├── list_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   ├── order_page.py
│   ├── home_page.py
│   ├── my_page.py
│   ├── login_page.py
│   └── VipPage.py
├── utils/                            # 트래킹/검증/연동 유틸
│   ├── NetworkTracker.py             # 네트워크 로그 수집·분류
│   ├── validation_helpers.py         # 정합성 검증
│   ├── urls.py                       # 환경별 URL (config.json의 environment 연동)
│   ├── credentials.py               # 로그인 계정
│   ├── frontend_helpers.py
│   └── google_sheets_sync.py
├── scripts/                          # 데이터 변환/검증 보조 스크립트
│   ├── json_to_sheets.py             # JSON → Google Sheets
│   ├── sheets_to_json.py             # Google Sheets → tracking_schemas JSON
│   └── compare_config_tracking.py
├── json/                             # 테스트 실행 시 생성되는 트래킹 로그 저장 (선택)
├── conftest.py                       # fixture, 브라우저 세션, TestRail 훅
├── pytest.ini                        # pytest 실행 설정
├── config.json                       # 실행 환경/TestRail/시트 설정 (environment, driver 등)
├── requirements.txt                  # 의존성 목록
├── Pipfile / Pipfile.lock            # pipenv 사용 시
└── README.md
```

## 🚀 설치 및 실행

### 필수 요구사항

- Python 3.11
- Playwright
- pytest
- pytest-bdd

### 설치

#### pip 사용

```bash
# 의존성 설치
pip install -r requirements.txt

# Playwright 브라우저 설치 (기본 브라우저)
playwright install
```

#### pipenv 사용

pipenv를 사용할 때는 **Pipfile**이 의존성 목록이므로 `requirements.txt`는 사용하지 않습니다.

```bash
# 의존성 설치 (Pipfile 기준)
pipenv install

# Playwright 브라우저 설치 (가상환경 안에서는 playwright install 만 하면 됨)
pipenv run playwright install
```

### 실행

테스트는 **환경별**로 `test/prod/` 또는 `test/dev/` 아래의 로더를 통해 실행합니다. 각 로더는 `features/prod/` 또는 `features/dev/`의 feature 파일을 참조합니다.

### 실행 전 `.env` 설정

테스트 실행 전 **프로젝트 루트**에 `.env` 파일을 두고, 아래 **변수 이름만** 맞춰 값을 채웁니다. 저장소에는 실 계정·비밀번호를 넣지 마세요.

**양식 예시** (값은 본인/팀 내부 정보로 교체):

```env
# TestRail (config.json에서 testrail_report = "Y" 일 때)
TESTRAIL_USERNAME=<TestRail_로그인_ID_또는_이메일>
TESTRAIL_PASSWORD=<TestRail_API_또는_비밀번호>

# 일반 회원 (prod·stg 등 기본 로그인 시나리오)
NORMAL_MEMBER_ID=<회원_ID>
NORMAL_MEMBER_PASSWORD=<회원_비밀번호>

# dev 전용 일반 회원 (config.json의 environment가 dev일 때 DEV_ 접두 키 우선 사용)
DEV_NORMAL_MEMBER_ID=<dev_회원_ID>
DEV_NORMAL_MEMBER_PASSWORD=<dev_회원_비밀번호>
```

#### pip 사용

```bash
# 운영(prod) 전체 시나리오 실행
pytest test/prod/ -v

# 개발(dev) 시나리오만 실행 (예: JFY)
pytest test/dev/test_jfy.py -v

# 특정 feature 로더만 실행
pytest test/prod/test_srp.py -v
pytest test/prod/test_pdp.py -v

# 로그 레벨 설정
pytest test/prod/ -v --log-cli-level=INFO

# 실행 결과를 화면과 파일에 동시에 저장 (Linux, macOS, Git Bash 등)
pytest test/prod/ -v 2>&1 | tee pytest.log
```

#### pipenv 사용

```bash
pipenv shell
pytest test/prod/ -v

# 또는
pipenv run pytest test/prod/ -v
pipenv run pytest test/dev/test_jfy.py -v
```

실행 결과를 **터미널과 동시에 로그 파일**에 남기려면 테스트 경로·파일명만 바꿔서 쓰면 됩니다.

```bash
# Linux, macOS, Git Bash 등 (`tee`: 화면 + 파일)
pipenv run pytest test/prod/ -v 2>&1 | tee pytest.log
```

```powershell
# Windows PowerShell (`Tee-Object`: 화면 + 파일, `*>&1` 로 stdout/stderr 모두 전달)
pipenv run pytest test/prod/ -v *>&1 | Tee-Object -FilePath pytest.log
pipenv run pytest --cache-clear test/dev/test_kotlin.py -v *>&1 | Tee-Object -FilePath pytest_kotlin.log
```

## ⚙️ 설정 파일

### config.json

프로젝트 루트의 `config.json`은 **실행 환경·TestRail·시트** 설정용입니다. `tracking_schemas/`(트래킹 검증 스키마)와는 별도입니다.

**주요 키:**
- `environment`: 실행 환경 (`"dev"` | `"stg"` | `"prod"`) — `utils/urls.py`에서 해당 환경 URL 사용
- `mobile_profile`: (선택) Playwright 모바일 에뮬레이션. `"iphone"`(기본) 또는 `"galaxy_s20"`(갤럭시 S20 이상·Android Chrome mweb). 생략 시 `iphone`
- `driver`: 브라우저 (예: `"Chrome"`)
- `match_rate`: 검증 시 허용 매칭률 (예: `0.88`)
- `testrail_report`: TestRail 보고 여부 (예: `"Y"` / `"N"`)
- `testrail_run_create`: (선택) TestRail Run 생성 여부 (`true`/`false`). `false`면 `testrail_run_id`의 기존 Run에만 기록
- `tr_url`, `project_id`, `suite_id`, `section_id`, `milestone_id`: TestRail 연동
- `testrail_run_id`: (선택) 기존 TestRail Run ID. 값이 있으면 새 Run을 만들지 않고 해당 Run에 결과 기록
- `spreadsheet_id`: Google Sheets 연동 시 스프레드시트 ID
- `case_id`: (선택) 테스트 케이스 ID 목록

예시:

```json
{
  "environment": "dev",
  "mobile_profile": "iphone",
  "driver": "Chrome",
  "match_rate": 0.88,
  "testrail_report": "N",
  "tr_url": "http://172.30.2.20",
  "project_id": "212",
  "suite_id": "1999",
  "section_id": "76275",
  "milestone_id": "1564",
  "spreadsheet_id": "1iv_ok0kTzWWPhzyRRbpEEnH3DPGE7VSJg2mmdlRPD78"
}
```

환경별 URL(base, cart, checkout, my 등)은 `utils/urls.py`에 정의되어 있으며, `config.json`의 `environment` 값에 따라 자동 선택됩니다.

### 영역별 트래킹 스키마 구조

트래킹 검증 스키마(JSON)는 영역·모듈별로 `tracking_schemas/` 아래에 있습니다:

```
tracking_schemas/
├── SRP/                    # Search Results Page
│   ├── 먼저 둘러보세요.json
│   ├── 일반상품.json
│   └── ...
├── LP/                     # List/Landing Page
├── PDP/                    # Product Detail Page
├── JFY/                    # JFY(이런 상품은 어때요)
├── HOME/
├── CART/
├── MY/
└── ORDER/
```

### 모듈 설정 파일 형식

각 모듈 설정 파일은 이벤트 타입별 섹션으로 구성됩니다:

```json
{
  "module_exposure": {
    "channel_code": "200003514",
    "cguid": "11412244806446005562000000",
    "spm-url": "gmktpc.home.searchtop",
    "spm-pre": "",
    "spm-cnt": "gmktpc.searchlist",
    "spm": "gmktpc.searchlist.cpc",
    "params-exp": {
      "parsed": {
        "module_index": "3",
        "ab_buckets": "mandatory"
      }
    }
  },
  "product_exposure": {
    "channel_code": "200003514",
    "spm": "gmktpc.searchlist.cpc",
    "params-exp": {
      "parsed": {
        "_p_prod": "<상품번호>",
        "utLogMap": {
          "query": "<검색어>",
          "origin_price": "<원가>",
          "promotion_price": "<할인가>",
          "coupon_price": "<쿠폰적용가>"
        }
      }
    }
  },
  "product_click": {
    ...
  },
  "pdp_pv": {
    ...
  }
}
```

### 플레이스홀더 및 특수 값 처리

#### 플레이스홀더

다음 플레이스홀더는 실제 값으로 자동 대체됩니다:

- `<상품번호>`: 실제 상품 번호로 대체
- `<검색어>`: 검색 키워드로 대체
- `<원가>`, `<할인가>`, `<쿠폰적용가>`: HTML에서 추출한 가격 정보로 대체
- `<environment>`: `config.json`의 `environment` 값 (예: `"prod"`, `"dev"`, `"stg"`)

#### 특수 값

- **`"mandatory"`**: 해당 필드는 반드시 값이 있어야 함 (값이 없으면 검증 실패)
- **`"skip"`**: 해당 필드는 검증을 수행하지 않음 (어떤 값이든 통과)
- **빈 문자열 `""`**: 정확히 빈 값이어야 함 (값이 있으면 검증 실패)
- **리스트 값 `["값1", "값2"]`**: 실제 값이 리스트 내 어느 값과든 일치하면 통과 (OR 조건)

자세한 필드 구조는 `tracking_schemas/` 내 JSON 파일과 `utils/validation_helpers.py` 주석을 참고하세요.

## 🔧 주요 컴포넌트

### NetworkTracker (`utils/NetworkTracker.py`)

네트워크 요청을 감지하고 트래킹 로그를 분류하는 클래스입니다.

**주요 메서드:**
- `start()`: 트래킹 시작
- `stop()`: 트래킹 중지
- `get_logs()`: 전체 로그 조회
- `get_module_exposure_logs_by_spm(spm)`: SPM으로 필터링된 Module Exposure 로그
- `get_product_exposure_logs_by_goodscode(goodscode, spm)`: 상품번호와 SPM으로 필터링된 Product Exposure 로그
- `get_product_click_logs_by_goodscode(goodscode)`: 상품번호로 필터링된 Product Click 로그
- `get_pdp_pv_logs_by_goodscode(goodscode)`: 상품번호로 필터링된 PDP PV 로그

**지원하는 이벤트 타입:**
- `PV`, `Module Exposure`, `Product Exposure`, `Product Click`, `Product ATC Click`, `PDP PV`

### SearchPage (`pages/search_page.py`)

검색 결과 페이지의 상호작용을 담당하는 Page Object Model입니다.

**주요 메서드:**
- `search_product(keyword)`: 키워드로 상품 검색
- `search_module_by_title(module_title)`: 모듈 타이틀로 모듈 찾기
- `assert_item_in_module(module_title)`: 모듈 내 상품 노출 확인 및 상품번호 반환
- `get_product_price_info(goodscode)`: 상품의 가격 정보 추출 (원가, 판매가, 할인률, 프로모션가, 쿠폰적용가)
- `click_product(goodscode)`: 상품 클릭 및 새 페이지 이동

### validation_helpers (`utils/validation_helpers.py`)

트래킹 로그의 정합성을 검증하는 헬퍼 함수들입니다.

**주요 함수:**
- `load_module_config(area, module_title, feature_path)`: 영역과 모듈명을 기반으로 설정 파일 로드
- `build_expected_from_module_config(module_config, event_type, ...)`: 모듈 설정에서 예상 값 생성
- `validate_event_type_logs(tracker, event_type, ...)`: 특정 이벤트 타입의 로그 검증 수행
- `replace_placeholders(expected_data, ...)`: 플레이스홀더를 실제 값으로 대체

### BrowserSession (`conftest.py`)

브라우저 세션 관리 클래스로, 현재 active page 참조를 관리합니다.

**주요 기능:**
- 페이지 스택을 통한 탭 전환 추적
- `page` 속성으로 현재 active page 접근
- `switch_to(page)`: 새 페이지로 전환
- `restore()`: 이전 페이지로 복귀

## 📖 사용 방법

### BDD Feature 파일 작성

Feature 파일은 Gherkin 문법을 사용하여 작성합니다:

```gherkin
Feature: G마켓 SRP 트래킹 로그 정합성 검증
  검색 결과 페이지에서 상품 클릭 시 트래킹 로그의 정합성을 검증합니다.

  Scenario: 검색 결과 페이지에서 모듈별 상품 클릭 시 트래킹 로그 검증
    Given G마켓 홈 페이지에 접속했음
    And 네트워크 트래킹이 시작되었음
    When 사용자가 "<keyword>"을 검색한다
    Then 검색 결과 페이지가 표시된다
    Given 사용자가 "<keyword>"을 검색했다
    And 검색 결과 페이지에 "<module_title>" 모듈이 있다
    When 사용자가 "<module_title>" 모듈 내 상품을 확인하고 클릭한다
    Then 상품 페이지로 이동되었다
    Then 모든 트래킹 로그를 JSON 파일로 저장함
    Then Module Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_module_exposure>)
    And Product Exposure 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_exposure>)
    And Product Click 로그가 정합성 검증을 통과해야 함 (TC: <tc_product_click>)
```

### 테스트 결과

테스트 실행 시 트래킹 로그를 저장하는 경우 `json/` 디렉토리에 예시와 같은 파일들이 생성될 수 있습니다:

- `tracking_pv_{goodscode}_{timestamp}.json`: PV 로그
- `tracking_module_exposure_*`, `tracking_product_exposure_*`, `tracking_product_click_*`, `tracking_pdp_pv_*`: 이벤트별 로그
- `tracking_all_{module_title}.json`: 전체 트래킹 로그 (모듈 타이틀 기준, 공백 등은 `_`로 치환)

## 🔗 TestRail 연동

프로젝트는 TestRail과 자동으로 연동되어 테스트 결과를 기록합니다.

### 주요 기능

1. **자동 Run 생성**: 테스트 세션 시작 시 `config.json`의 `section_id` 기반으로 TestRail Run 자동 생성
   - `testrail_run_create=false`면 Run 생성 없이 `testrail_run_id` 기존 Run에 바로 기록
2. **스텝별 결과 기록**: 각 BDD 스텝 실행 후 TestRail에 결과 자동 기록
3. **TC 번호 추출**: 스텝 파라미터에서 TC 번호 (예: `C12345`) 자동 추출
4. **스크린샷 첨부**: 실패 시 자동으로 스크린샷 캡처 및 첨부
5. **로그 첨부**: 실행 로그를 TestRail 결과에 자동 첨부
6. **Soft Assertion 지원**: 프론트엔드 실패나 검증 실패를 구분하여 기록

### 설정

TestRail 연동을 위해서는 `config.json`에 TestRail 설정이 필요합니다:

```json
{
  "tr_url": "http://172.30.2.20",
  "project_id": "212",
  "suite_id": "1999",
  "section_id": "69751",
  "milestone_id": "1564",
  "testrail_run_create": true,
  "testrail_run_id": ""
}
```

**참고**: TestRail 인증 설정 방법은 내부 문서를 참고하세요.

## 📊 Google Sheets 데이터 관리

프로젝트는 Google Sheets를 통한 설정 파일 관리를 지원합니다.

### 주요 기능

1. **JSON → Google Sheets**: `tracking_schemas/schema_template.json`에 정의된 **경로(트리)만** 시트에 쓰고, 각 셀 값은 `tracking_all` 로그에서 역으로 채운다 (`scripts/json_to_sheets.py`).
2. **Google Sheets → JSON**: Google Sheets에서 편집한 데이터를 트래킹 스키마(tracking_schemas) JSON 파일로 변환

### 사용 방법

```bash
# JSON → Google Sheets
python scripts/json_to_sheets.py \
  --input json/tracking_all_먼저_둘러보세요.json \
  --module "먼저 둘러보세요" \
  --area SRP

# 파일명이 tracking_all_<모듈>(선택적 (숫자)).json 이면 --module 생략 가능
python scripts/json_to_sheets.py \
  --input json/tracking_all_today_branddeal(1).json \
  --area KOTLIN

# Google Sheets → JSON
python scripts/sheets_to_json.py \
  --module "먼저 둘러보세요" \
  --area SRP \
  --overwrite
```

상세한 옵션은 각 스크립트의 `--help`를 참고하세요.

## 📝 주의사항

1. **상품 클릭 전 가격 정보 추출**
   - `get_product_price_info()`는 상품 클릭 전에 호출해야 합니다.
   - 상품 클릭 후에는 페이지가 이동하여 HTML 요소에 접근할 수 없습니다.

2. **SPM 필터링**
   - Module Exposure와 Product Exposure 로그는 SPM 값으로 필터링됩니다.
   - 영역별 설정 파일에 올바른 SPM 값이 설정되어 있어야 합니다.

3. **로그 저장**
   - 테스트 실행 중 네트워크 요청이 완료될 때까지 충분한 대기 시간을 확보해야 합니다.
   - `time.sleep(2)` 또는 `page.wait_for_load_state('networkidle')` 사용을 권장합니다.

4. **환경·영역 구분**
   - `config.json`의 `environment`로 dev/stg/prod가 결정되며, URL은 `utils/urls.py`에서 선택됩니다.
   - Feature 파일명이 `{area}_tracking.feature` 형식이면 영역 자동 추론이 작동합니다 (예: `srp_tracking.feature` → `SRP`).

5. **브라우저 실행/로그인 상태 파일**
   - 기본 설정은 `headless=False`로 동작하여 실행 시 브라우저 창이 표시됩니다.
   - 세션 시작 시 로그인 후 `state.json`을 생성(또는 갱신)해 테스트 컨텍스트에 사용합니다.

## 🐛 문제 해결

### 로그가 수집되지 않는 경우

1. 네트워크 트래킹이 시작되었는지 확인 (`tracker.start()`)
2. 페이지 로딩이 완료되었는지 확인
3. `aplus.gmarket.co.kr` 도메인으로의 요청이 발생하는지 확인

### 정합성 검증 실패

1. 영역별 설정 파일의 플레이스홀더가 올바르게 설정되었는지 확인
2. `frontend_data`에 필요한 가격 정보가 포함되어 있는지 확인
3. SPM 값이 올바른지 확인
4. 특수 값 처리 (`mandatory`, `skip`, 리스트 값) 확인

### TestRail 연동 문제

1. `config.json`의 TestRail 설정이 올바른지 확인
2. TestRail 인증 설정이 올바른지 확인 (내부 문서 참고)

### Google Sheets 동기화 문제

1. 서비스 계정 JSON 파일이 프로젝트 루트에 있는지 확인
2. 구글 시트에 서비스 계정 이메일이 공유되어 있는지 확인
3. `scripts/json_to_sheets.py --help`, `scripts/sheets_to_json.py --help` 옵션 확인

## 📚 참고 파일

| 파일 | 역할 |
|------|------|
| `config.json` | 실행 환경, TestRail, 시트 설정 (트래킹 스키마와 별도) |
| `tracking_schemas/` | 트래킹 이벤트 검증용 스키마(JSON) |
| `conftest.py` | fixture, 브라우저 세션, TestRail 훅 |
| `utils/NetworkTracker.py` | 네트워크 로그 수집·분류 |
| `utils/validation_helpers.py` | 정합성 검증 로직 |
| `utils/urls.py` | 환경별 URL (config.json의 `environment` 연동) |

## 📄 라이선스

이 프로젝트는 내부 사용을 위한 것입니다.
