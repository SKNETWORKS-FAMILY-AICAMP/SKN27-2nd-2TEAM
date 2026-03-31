# 작업 히스토리

## 2026-03-31

### 1) 홈 KPI 카드 기능 개편
- KPI 데이터 소스를 고정 CSV에서 `netflix_user_sample.csv` 기반 동적 집계로 전환.
- KPI 기준일/비교일 설정을 `config` 상수로 분리:
  - `KPI_TARGET_MONTH_DAY`
  - `KPI_DELTA_DAYS`
  - `KPI_INACTIVE_DAYS_THRESHOLD`
- KPI 카드 표시를 설정 기반으로 전환:
  - 제목/아이콘/스타일/증감 해석을 `ui_config.json`의 `dashboard.kpi_cards`에서 관리.
  - 카드 컬럼 수를 `dashboard.kpi_layout.columns`로 외부화.

### 2) KPI 지표/표시 규칙 조정
- KPI 타이틀 한글화 적용.
- 단위 한글화 적용 (`분`, `일`).
- 3번째 KPI를 이탈률 중심에서 활성 유저 비율 중심으로 표시되도록 정리.
- 활성 유저 비율 증감 계산/표시 방향 오류 수정:
  - 감소 시 음수로 표시되도록 `ui_config.json`의 delta 해석 규칙 보정.
- 평균 미접속 기간 카드의 증감 색상 기준 반전:
  - 증가(양수)는 부정 신호로 빨간색 표시.

### 3) 분석 화면 리팩토링 (함수 분해/설정화)
- `analysis_outcomes` 분해:
  - 델타 뷰모델 계산, KPI 2열 렌더, 히스토그램 렌더, AI 요약 렌더로 분리.
- `analysis_simulator` 분해:
  - 구독 필드/행동 필드/폼 payload 수집 함수로 분리.
  - 휴리스틱 계수와 범위를 `ui_config.json`의 `analysis.simulator_heuristics`로 외부화.
- `analysis` 화면 조립 분해:
  - 페이지 설정 로드, 세그먼트 선택, 결과 렌더 보조 함수로 분리.

### 4) 레이아웃/차트 설정 외부화
- 분석 화면 레이아웃 수치 외부화:
  - `analysis.layout.columns`, `analysis.layout.gap`
  - `analysis.layout.histogram_height`
  - `analysis.layout.results_top_spacer`, `results_section_spacer`
- 분석 위험 임계값 외부화:
  - `analysis.thresholds.high_risk_churn_prob`
- 홈 트렌드 차트 높이 외부화:
  - `charts.trend_section.height`

### 5) 디자인 코드 정리
- `design/common.py`, `design/metrics.py`, `design/charts.py`, `design/sidebar.py`를 섹션 함수로 분리.
- 반복 색상값을 `COLORS` 토큰 기반으로 통일(하드코딩 hex 축소).
- `markup.py` 내 다수 색상 fallback/인라인 색상을 토큰 참조로 정리.

### 6) 주석 정리
- 주요 파일의 함수/핵심 변수에 기능 설명 주석 추가:
  - `src/utils/data_loader.py`
  - `src/screens/analysis.py`, `src/screens/dashboard.py`
  - `src/components/*` 주요 파일
  - `src/design/*` 주요 파일
  - `src/utils/churn_histogram.py`

### 7) 홈 하단 데이터 정보 카드 교체
- `src/config/dashboard_modules.json` 하단 3개 카드 내용 데이터 기반으로 교체.
- 구독 플랜 분포를 샘플 데이터 비율 기반으로 조정:
  - Standard 40%
  - Premium 30%
  - Basic 30%
- `churn_reasons` 카드를 정성 사유 목록에서 행동 지표 카드로 전환:
  - 평균 완주율 64.53%
  - 추천 클릭률 평균 49.56%
  - 멀티 디바이스 이용 비중 66.48%
  - 하이 빈지 사용자 비중 33.57%
- `recent_sessions` 카드를 데이터셋 커버리지/품질 요약 카드로 전환:
  - 국가 커버리지 10개국
  - 장르 카테고리 8개
  - 결제수단 유형 4개
- 초기 반영했던 `결측치: 0건` 항목은 요구사항에 따라 제거.

### 8) 사이드바 컬러 톤 조정
- `src/design/sidebar.py` 사이드바 배경/텍스트 대비를 다크-미드 톤으로 재설정.
- 단계별 요청 반영으로 최종 배경색을 `#475569`로 조정.
- hover/선택 상태 배경 및 텍스트 대비를 함께 보정해 열림 상태 가독성 개선.

---

## 기록 규칙
- 같은 날짜 작업은 이 파일의 해당 날짜 섹션 아래에 계속 누적.
- 날짜가 바뀌면 `## YYYY-MM-DD` 섹션을 새로 추가.
- 항목은 `기능 변경 / 리팩토링 / 설정 외부화 / 버그 수정 / 주석 정리` 단위로 기록.
