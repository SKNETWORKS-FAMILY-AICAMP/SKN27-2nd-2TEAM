# 대시보드 UI 및 데이터 모듈화

## 작업 일자
2026년 03월 28일

## 작업 목적
- 하드코딩되어 있던 대시보드의 표시 정보(UI 텍스트, 설명 등) 및 샘플 데이터(차트, 지표)를 분리하여 동적으로 관리할 수 있도록 구조 개선
- 향후 데이터베이스 연동이나 설정 변경 시 소스코드 수정 없이 데이터 파일만 수정하여 반영할 수 있도록 모듈화 기반 마련

## 작업 내역
1. **환경 설정 및 경로 모듈화 (`src/config.py`)**
   - `data/sample` 디렉토리를 참조하도록 데이터 및 UI 설정 경로 추가 (`UI_CONFIG_PATH`, `METRICS_DATA_PATH`, `CHART_DATA_PATH`)

2. **샘플 데이터 파일 분리 생성 (`data/sample/`)**
   - `ui_config.json`: 화면 별 헤더 제목, 설명, 사이드바 메뉴명, 드롭다운 옵션 등 공통 텍스트 관리
   - `metrics.json`: 대시보드 상단 4개의 KPI 지표(총 고객 수, 활성 유저, 이탈률, 수익 등) 수치, 아이콘, 증감률 관리
   - `chart_data.csv`: 메인 트렌드 차트에 그려질 활성 사용자 시계열 데이터 관리

3. **데이터 로더 유틸리티 작성 (`src/utils/data_loader.py`)**
   - JSON 및 CSV 데이터를 파싱하는 함수 구현
   - `Streamlit`의 `@st.cache_data`를 활용하여 불필요한 반복적인 파일 I/O를 방지하도록 캐싱 로직 적용

4. **UI 컴포넌트 데이터 연동**
   - `src/components/sidebar.py`: `ui_config.json`을 읽어와 동적으로 메뉴 및 사이드바 텍스트 구성
   - `src/screens/dashboard.py`, `analysis.py`, `model.py`: 화면별 페이지 헤더 및 설명 텍스트 연동
   - `src/components/metrics.py`: `metrics.json`을 기반으로 반복문(loop)을 통한 KPI 카드 렌더링 적용
   - `src/components/charts.py`: `chart_data.csv`의 데이터를 DataFrame으로 로드하여 `st.line_chart` 렌더링에 적용

## 2026년 03월 28일 추가 작업 내역
- **config 구조 개편**: `data/sample` 디렉토리에 위치해 있던 UX/UI 관련 구성용 파일(`ui_config.json`, `metrics.json`)을 단순 데이터 파일과 구분하기 위해 `src/config` 디렉토리로 이동시켰습니다.
- **경로 관리 스크립트 이동**: `src/config.py` 파일도 `src/config/config.py`로 이동시키고, 내부 파일 경로 및 관련 import 문(`src/utils/data_loader.py` 등)들을 업데이트했습니다.

## 2026년 03월 28일 추가 작업 내역 (페이지 설정 모듈화)
- **`st.set_page_config` 분리**: 브라우저 탭 제목·파비콘(이모지)·레이아웃·초기 사이드바 상태를 [`src/config/ui_config.json`](../../src/config/ui_config.json) 최상위 키 `app`에 정의했습니다 (`page_title`, `page_icon`, `layout`, `initial_sidebar_state`).
- **적용 함수**: [`src/design/styles.py`](../../src/design/styles.py)에 `apply_streamlit_page_config()`를 추가해 `load_ui_config()`로 `app` 블록을 읽은 뒤 `st.set_page_config`를 호출합니다. 앱 엔트리 [`main.py`](../../main.py)에서는 해당 함수만 호출하도록 정리했습니다.

## 2026년 03월 28일 HTML 마크업 집약 (별도 기록)
- `st.html`용 HTML 조각을 [`src/design/markup.py`](../../src/design/markup.py)로 모으고, 대시보드 하단 3모듈 데이터는 [`data/sample/dashboard_modules.json`](../../data/sample/dashboard_modules.json), 분석 화면 비교/AI 문구는 `ui_config.json`의 `analysis.compare_cards`·`ai_comment` 등으로 이전했습니다. 상세 체크리스트·비고는 [`docs/plans/front_html_markup_refactor.md`](front_html_markup_refactor.md)를 참고하세요.

## 향후 계획
- 루트 디렉토리의 `data/sample` 폴더를 활용하여 구조를 정립 완료.
- 추후 실제 API 또는 DB를 통해 데이터를 받아올 때, `src/utils/data_loader.py`의 유틸리티 로더 내부 로직만 수정하면 화면 코드 수정 없이 손쉽게 연동이 가능합니다.