# HTML 마크업 design 집약 작업 기록

## 작업 목적

- `st.html`에 흩어진 HTML 문자열을 `src/design/markup.py`로 모아 가독성과 유지보수성을 높임.
- 대시보드 하단 3모듈의 문구·수치는 `data/sample/dashboard_modules.json`으로 분리.
- 분석 화면의 고정 한글 문구는 `ui_config.json`의 `analysis` 하위 키로 이전.

## 작업 일자

2026년 03월 28일

## 진행 체크리스트

- [x] 본 기록 파일 생성 (`docs/plans/front_html_markup_refactor.md`)
- [x] `data/sample/dashboard_modules.json` 추가 및 `config` / `data_loader` 연동
- [x] `ui_config.json`에 `compare_cards`, `ai_comment`, `form.section_icon` 반영
- [x] `src/design/markup.py` 구현
- [x] `dashboard.py`, `analysis.py`, `sidebar.py`, `charts.py`, `metrics.py`, `dashboard_modules.py` 연동
- [x] `python -c`로 import 스모크 확인 (Streamlit 캐시 경고만 발생)

## 산출물 요약

| 구분 | 경로 |
|------|------|
| 마크업 조립 | `src/design/markup.py` |
| 하단 모듈 데이터 | `data/sample/dashboard_modules.json` |
| 분석 화면 문구 | `src/config/ui_config.json` (`analysis.compare_cards`, `analysis.ai_comment`, `form.section_icon`) |
| 경로 상수 | `src/config/config.py`의 `DASHBOARD_MODULES_DATA_PATH` |
| 로더 | `src/utils/data_loader.py`의 `load_dashboard_modules_data()` |

## 연동 요약

- 화면/컴포넌트는 `from src.design import markup` 후 `st.html(markup....)` 패턴으로 통일.
- KPI 비교 카드·AI 코멘트 문구는 JSON에서 바꾸면 코드 수정 없이 반영 가능.
- 하단 3모듈은 `dashboard_modules.json`의 `plan_distribution` / `churn_reasons` / `recent_sessions` 구조를 따름.

## 비고

- 사용자·CSV에서 오는 값(세그먼트명 등)은 `html.escape`로 이스케이프 후 삽입.
- 색상 코드는 `#` + 6자리 hex만 허용(`_safe_hex_color`), 그 외는 fallback.
- Jinja 등 추가 의존성 없음.
