---
name: 시뮬레이터 세그먼트 데이터 재설계
overview: "`netflix_user_sample.csv` 원본에서 의미 있는 수동 세그먼트를 생성하고, 세그먼트별 피처 기본값(수치=평균, 타입=최빈값)을 산출해 `simulator_sample.csv`를 재구성합니다. 동시에 현재 코드가 의존하는 `base_churn_prob` 중심 구조를 피처 기본값 중심 구조로 전환합니다."
todos:
  - id: define-segments
    content: 원본 데이터 기준 4~6개 수동 세그먼트 조건식 정의
    status: pending
  - id: build-segment-defaults
    content: 세그먼트별 수치 평균/타입 최빈값 집계 및 simulator_sample.csv 재작성
    status: pending
  - id: refactor-analysis-schema
    content: analysis.py와 analysis_simulator.py에서 base_churn_prob 의존 제거 및 새 스키마 연결
    status: pending
  - id: sync-ui-config
    content: ui_config.json 폼 옵션/라벨을 새 스키마와 정합화
    status: pending
  - id: validate-runtime
    content: 로딩/렌더링/폼 기본값 동작 검증 및 lint 점검
    status: pending
---

# 시뮬레이터 세그먼트 데이터 재설계

## 목표

- 원본 사용자 데이터([c:/dev/project/SKN27-2nd-2TEAM/data/sample/netflix_user_sample.csv](c:/dev/project/SKN27-2nd-2TEAM/data/sample/netflix_user_sample.csv))를 기준으로 4~6개의 의미 있는 수동 세그먼트를 정의합니다.
- 세그먼트별 기본값을 `수치형=평균`, `타입형=최빈값(mode)` 규칙으로 계산해 [c:/dev/project/SKN27-2nd-2TEAM/data/sample/simulator_sample.csv](c:/dev/project/SKN27-2nd-2TEAM/data/sample/simulator_sample.csv)에 반영합니다.
- 시뮬레이터 입력/표시가 `base_churn_prob` 의존 없이 피처 기본값 중심으로 동작하도록 [c:/dev/project/SKN27-2nd-2TEAM/src/screens/analysis.py](c:/dev/project/SKN27-2nd-2TEAM/src/screens/analysis.py), [c:/dev/project/SKN27-2nd-2TEAM/src/components/analysis_simulator.py](c:/dev/project/SKN27-2nd-2TEAM/src/components/analysis_simulator.py), [c:/dev/project/SKN27-2nd-2TEAM/src/config/ui_config.json](c:/dev/project/SKN27-2nd-2TEAM/src/config/ui_config.json)을 정합성 있게 조정합니다.

## 구현 접근

- 세그먼트 정의(초안, 4~6개)
  - 예: 신규 사용자군, 장기 충성군, 고시청 저문의군, 저시청 고문의 위험군 등으로 조건식을 명시합니다.
  - 각 세그먼트는 `netflix_user_sample.csv`의 원본 row 집합(필터 조건)으로 표현합니다.
- 집계 규칙 적용
  - 수치형: `monthly_fee`, `avg_watch_time_minutes`, `content_interactions` 등 후보에서 시뮬레이터 컬럼과 매핑 가능한 값만 평균 산출.
  - 타입형: `subscription_type` 포함 타입 컬럼은 세그먼트 내 최빈값 적용.
- 시뮬레이터 스키마 재정의
  - `base_churn_prob` 제거 또는 비활성화.
  - `feature_defaults_only` 합의에 맞게 입력 기본값 컬럼만 유지.
  - 화면/컴포넌트가 참조하는 컬럼명과 CSV 스키마를 일치시킵니다.
- UI/로직 조정
  - [c:/dev/project/SKN27-2nd-2TEAM/src/components/analysis_simulator.py](c:/dev/project/SKN27-2nd-2TEAM/src/components/analysis_simulator.py): 기준값 비교 로직을 새로운 기본값 컬럼 기준으로 재연결.
  - [c:/dev/project/SKN27-2nd-2TEAM/src/screens/analysis.py](c:/dev/project/SKN27-2nd-2TEAM/src/screens/analysis.py): 결과 계산 진입부에서 `base_churn_prob` 의존 제거.
  - [c:/dev/project/SKN27-2nd-2TEAM/src/config/ui_config.json](c:/dev/project/SKN27-2nd-2TEAM/src/config/ui_config.json): 폼 옵션/라벨이 새 스키마와 충돌하지 않도록 점검.
- 검증
  - 샘플 CSV 로드 성공 및 세그먼트 선택 정상 동작 확인.
  - 폼 기본값이 세그먼트별 집계 결과(평균/최빈값)로 반영되는지 확인.
  - 관련 파일 lint 에러 점검 및 수정.

## 변경 대상 파일

- 데이터
  - [c:/dev/project/SKN27-2nd-2TEAM/data/sample/simulator_sample.csv](c:/dev/project/SKN27-2nd-2TEAM/data/sample/simulator_sample.csv)
- 앱 로직
  - [c:/dev/project/SKN27-2nd-2TEAM/src/screens/analysis.py](c:/dev/project/SKN27-2nd-2TEAM/src/screens/analysis.py)
  - [c:/dev/project/SKN27-2nd-2TEAM/src/components/analysis_simulator.py](c:/dev/project/SKN27-2nd-2TEAM/src/components/analysis_simulator.py)
- 설정
  - [c:/dev/project/SKN27-2nd-2TEAM/src/config/ui_config.json](c:/dev/project/SKN27-2nd-2TEAM/src/config/ui_config.json)

## 수용 기준

- `segment_name`은 원본 row 그룹 기반으로 정의되고, 각 세그먼트가 1개 이상 row를 가집니다.
- 세그먼트 기본값은 수치형 평균/타입형 최빈값 규칙을 만족합니다.
- 시뮬레이터가 `base_churn_prob` 없이도 화면 오류 없이 렌더링/조정됩니다.
- 기존 분석 화면 UX(세그먼트 선택 -> 파라미터 조정 -> 결과 확인) 흐름이 유지됩니다.
