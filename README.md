# 🎬 SKN27-2ND-2TEAM 프로젝트
## 넷플릭스를 이탈하던 어둠의 유저들은 이미 소멸하였다. 균열된 해지의 문은 봉인되었고, 저주받은 매출은 회복되어 풍요를 되찾았다. 넷플릭스의 깃발은 지평선 끝까지 휘날리며, 부와 콘텐츠는 우리의 손 안에 온전히 귀속되었다. 이 모든 업적은 오직 젠틀핑, 뿌뿌핑, 말랑핑, 왕자핑, 젠틀핑, 믿어핑, 트러핑의 5명의 용사, 바로 머신러닝과 우리에 의해 완수되었다.

https://github.com/user-attachments/assets/e2a069c2-8be5-44cc-bbef-758de055b4d4


### 2차 프로젝트: 넷플릭스 고객 이탈 분석 및 예측
**개발 기간:** 2026.03.25 - 2026.04.02
---

## 팀 소개

**팀명: 2조**
|![title](https://i.namu.wiki/i/EXUFV0Tuo0cLyoVpeGuFe-h6azQ92PWnT4uGLMgaT9rq0_cLEtXTNHwPrQlGO95CmS2p7Kha0_JZfuiLth0LF3cuEYrOtXeYHx5oKBvpiiXlovpq6gdNPVCGLZY-jauHab6SZNfspKLfi41-4pt6rw.webp)|![title](https://i.namu.wiki/i/ys-84JzsMzI14JysdBiTVoE-KISPvw5XxZvoapBEPsDrgnDfUsRiuLBt_CvlvbgYn-5By7p5kmlwBxUxr61Mvk5TpzpFMxtWst5IEcypDVrezIkd7EpA3zVztFkx2C90pW2pbpP1_2W98Wh0m3km3w.webp)|![title](https://i.namu.wiki/i/7hBaLlK5N0Y-ucvkzGzaoJ62jfGkeuw7YUp2BC5c2ohVtk3lrws3sMu4t74Uoqo8alfO3jQzIGpfLZTQjAmTwHDW-xBc52KwAjrknLz849jCG4GwfxtzTYGVARqdUiL4_fD6G4F9YbOQdBVSNWdinA.webp)|![title](https://i.namu.wiki/i/50kcgE_FPjKqBakTzT27J7gDH1EK6Yws9qOAP6tHXYXBmeJlqw5S4crlHDua-GhDdfvX6KGfmb6aY9NvtdkhwvS5Fpk-BrkO8EB4xxSmnYqjDvs7kqqXt_feZXdzyR9I_6zV1dlRoEmbv-UVSgRxxA.webp)|![title](https://i.namu.wiki/i/nk7nENfy3WH03XgdEuokWEwr4O7uUlP1A2SLmRE5zoFNCOiDBRZJXsW-xe3cuSZLFujpGrbv8-exsnyer3RlzVrJZe7IBXuXubdSkIcOP6ZIHnpRq4y5Gt0mXqZfF-6c9DHpPjUtEXS7YxLoYakQIA.webp)|![title](https://i.namu.wiki/i/JcP5JyejZmiSzJFFu9a3VnwAViYqyuaukpcW4Ixk-Od90MVCCBfXxt4uU88uJ0Cn9Az5kNLDK8G6QDHeab61H7ZSFR0llJ74EiiFc75QPsp5Og8HtQiSxYvXWFTeE5LwtYhycNwCEcbiV-JKCB8euw.webp)|
|:---:|:---:|:---:|:---:|:---:|:---:|
| **김경수 (팀장)** | **김주영** | **문재경** | **이성진** | **이재강** | **이재건** |
| UI, 스트림릿 구현 | 데이터 전처리 | 모델링 및 검증 | 베이스 모델 | 데이터 전처리 | 모델링 및 검증 |

---

## 1. 프로젝트 개요
> <img width="512" alt="8ed5a8dc-87e8-4839-9299-7a76b65fdfe4" src="https://github.com/user-attachments/assets/ba3301a1-ac05-416a-8937-e2257d052866" />

>
> OTT 시장의 경쟁 심화로 인해 신규 고객 유치보다 기존 고객의 유지(Retention)가 기업 성장의 핵심 지표가 됨. 본 프로젝트는 Kaggle의 넷플릭스 유저 데이터를 활용하여 시청 패턴, 구독 정보, 기기 사용 습관을 분석하고 **이탈 가능성이 높은 유저를 사전에 식별**하는 예측 모델 구축을 목표.

### 1.2. 프로젝트 소개
* **데이터 통합:** 6개의 분산된 CSV 파일을 결합하여 유저별 통합 프로필 구축.
* **이탈 예측 모델링:** DecisionTree, XGBoost 등 다양한 알고리즘을 통한 이탈 징후 포착.
* **전략적 인사이트:** 파생 변수(완독률, 시간당 비용 등)를 통해 고객의 페인 포인트(Pain Point) 도출.

### 1.3. 프로젝트 목표
1.  **이탈 징후 포착:** 완독률 및 시간당 비용 등 핵심 지표를 통한 이탈 예측.
2.  **데이터 정제:** 불완전한 사용자 데이터를 비즈니스 로직에 기반하여 정밀 복구.
3.  **인사이트 도출:** 어떤 요소가 고객을 떠나게 만드는지 상관관계 및 모델 중요도 분석.

---

## 🛠 기술 스택

<p>
  <img src="https://img.shields.io/badge/python-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/seaborn-444444?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white"/>
  <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
</p>

---

## 2. 데이터

- **수집 환경**: 도커 컨테이너(Docker Container) 상에서 Kaggle 데이터셋을 다운로드하였습니다.
- **수집 전처리**: 원본 데이터에서 중복 값을 제거하고, 문자열로 된 ID 데이터(예: `user_0001`)를 정수형(`1`)으로 일괄 변환하여 DB에 적재했습니다.

### 원본 데이터 구성

프로젝트에 사용된 원본 데이터는 총 6개의 테이블로 구성됩니다.

| 테이블명              | 주요 정보                                                       |
| --------------------- | --------------------------------------------------------------- |
| `users`               | 사용자 기본 정보 및 구독 정보 (이탈 여부 예측의 타겟 변수 포함) |
| `watch_history`       | 콘텐츠 시청 로그                                                |
| `movies`              | 콘텐츠 메타 데이터                                              |
| `recommendation_logs` | 시스템 추천 로그                                                |
| `search_logs`         | 검색 로그                                                       |
| `reviews`             | 콘텐츠 리뷰 정보                                                |

### ERD
<img width="1280" height="1795" alt="image" src="https://github.com/user-attachments/assets/4a07d2c5-cb14-4247-83e3-f4c8764b7c77" />

---

## 2-1. EDA 및 피처 엔지니어링

### 

### 독립변수 구성 (Total 17개)
6개의 원본 데이터(사용자, 시청 기록, 콘텐츠, 추천/검색 로그, 리뷰)를 결합하여 유저의 행동 패턴과 경제적 가치를 분석하기 위한 변수들을 아래와 같이 구성하였습니다.

| 구분 | 변수명 | 설명 및 산출 근거 |
|:---:|:---|:---|
| **기존 변수** | `age`, `gender`, `country`, `sub_type`, `device`, `fee` | 유저 기본 프로필(나이, 성별, 국가) 및 구독 정보(유형, 기기, 요금) |
| **가공 변수** | **계정 생성 개월수** <br> `account_age_months` | 가입일로부터 현재까지의 유지 기간 계산 |
| | **사용 기기 수** <br> `devices_used` | 로그 데이터 내 유저별 고유 기기(Device) 종류 카운트 |
| | **선호 장르** <br> `favorite_genre` | 유저 시청 기록 중 가장 빈도가 높은 메인 장르 (최빈값) |
| **파생 변수** | **추천 클릭률** <br> `rec_click_rate` | 유저에게 노출된 추천 콘텐츠 중 실제 클릭으로 이어진 비율 (%) |
| | **콘텐츠 상호작용 수** <br> `content_interactions` | 리뷰 작성 + 추천 클릭 + 검색 클릭의 총합 (유저 능동성 지표) |
| | **주간 평균 세션 수** <br> `watch_sessions_per_week` | 유저의 주간 평균 접속 및 시청 횟수 (정수형) |
| | **일일 평균 시청 시간** <br> `avg_watch_time_minutes` | 유저의 일평균 콘텐츠 시청 시간 (분 단위) |
| | **완독률** <br> `completion_rate` | 전체 시청 시도 중 '완료(Completed)' 혹은 진척도 100%인 비율 (%) |
|  | **평균 부여 평점** <br> `rating_given` | 유저가 남긴 리뷰 평점의 평균값 (정수형 반올림) |
| | **시간당 비용** <br> `cost_per_hour` | `월 요금 / (총 시청 시간 / 60)` (클수록 유저가 체감하는 비용 부담↑) |
| | **시청 완료 여부** <br> `is_completed` | 개별 시청 기록의 완료 상태 여부 (이진 지표 0/1) |

---

### 핵심 파생 변수 생성 로직
* **시청 완독률 (`completion_rate`):** 단순 시청 여부를 넘어 콘텐츠를 끝까지 소비했는지를 측정하여 서비스에 대한 실질적인 몰입도를 파악합니다.
* **시간당 비용 (`cost_per_hour`):** 유저가 지불하는 구독료 대비 실제 이용 시간을 계산하여, '가성비'에 따른 심리적 이탈 요인을 수치화합니다.
* **상호작용 지표 (`content_interactions`):** 리뷰나 검색 클릭 등 능동적인 행동을 통합하여, 단순 시청자(Passive)와 충성 고객(Active)을 식별하는 지표로 활용합니다.


> ><img width="1127" height="939" alt="스크린샷 2026-04-01 120626" src="https://github.com/user-attachments/assets/fe040430-eea3-4f79-87f6-2fe191cf22ff" />

> 

---

## 3. 데이터 전처리

### 결측값 처리 전략 (Missing Value Handling)
데이터의 특성(수치형, 범주형, 날짜형)과 비즈니스 로직을 고려하여 아래와 같이 결측치를 보정

| 변수명 | 처리 방법 | 처리 이유 |
|:---|:---|:---|
| **Age** | 중앙값(Median) 대체 | 100세 이상 등 이상치 존재를 고려한 보수적 대치 |
| **Gender** | 비율 기반 랜덤 할당 | Male, Female, Other, Unknown 비율을 유지하며 결측치 보정 |
| **Monthly Fee** | 구독 유형별 최소값 대치 | Basic(10)~Premium+(25) 기준 비즈니스 로직 적용 |
| **Completion Rate** | 0으로 대치 | 시청 기록 부재 시 서비스 미이용자로 판단하여 0% 처리 |
| **Cost per Hour** | 보정값(0.1) 추가 후 0 처리 | 분모가 0이 되어 무한대(inf)가 발생하는 현상 방지 |
| **Rec Click Rate** | 0으로 대치 | 추천 로그가 없는 유저는 클릭 활동이 없으므로 0% 처리 |
| **Interactions** | 0으로 대치 | 리뷰/추천/검색 기록이 없는 경우 활동 수 0으로 합산 |
| **Rating Given** | 0으로 대치 | 리뷰를 한 번도 남기지 않은 유저는 부여 평점 0점으로 처리 |
| **Watch Metrics** | 0으로 대치 | 주간 세션 및 일일 시청 시간이 없는 경우 미시청(0)으로 간주 |
| **Days Since Last** | 0으로 대치 | 모든 활동 로그가 없는 신규/휴면 유저는 경과일 0으로 처리 |
| **Favorite Genre** | **'Unknown'** 대체 | 시청 기록이 없어 선호 장르 판별이 불가능한 경우 문자열 할당 |

---

### 데이터 정제 및 변환 원칙

**1. 수치형 피처 (Activity-based Features)**
대부분의 파생 변수는 특정 활동 로그가 없는 유저의 경우 `NaN`이 발생. 이를 **활동이 전혀 없었음(0)**으로 간주하여 모델이 학습할 수 있는 수치로 변환.
* 대상: 추천 클릭률, 상호작용 수, 평균 평점, 완독률, 시청 시간 등

**2. 범주형 피처 (Categorical Features)**
선호 장르(`favorite_genre`)와 같이 유저의 취향을 나타내는 변수 중 데이터가 없는 경우, 임의의 장르를 배정하지 않고 **'Unknown'**이라는 새로운 범주를 생성하여 데이터의 순수성을 유지.

**3. 날짜 및 타입 변환 (Data Type Casting)**
* **pd.to_datetime (errors='coerce'):** 날짜 형식이 잘못되었거나 비어있는 경우 `NaT`로 변환한 뒤, 이후 계산 과정에서 기준일과의 차이를 구하여 0 또는 특정 기간 값으로 보정.
* **타입 최적화:** 연산의 효율성을 위해 비율 데이터는 100을 곱한 뒤 정수형(`int`)으로 변환하여 모델의 연산 속도를 높여짐.

* **인코딩:** 5개 범주형 변수에 `OneHotEncoding` 적용 (18개 → 48개 컬럼 확장)
* **이상치:** IQR 방식을 통해 `devices_used`(20.91%) 등 주요 변수 이상치 탐지

> <img width="1500" height="688" alt="572408866-69351573-1a7c-49df-8251-add9b004d21a" src="https://github.com/user-attachments/assets/2488ed50-3ad6-4476-86d6-47ee939a7268" />

> <img width="996" height="791" alt="스크린샷 2026-04-01 145724" src="https://github.com/user-attachments/assets/37bfec6c-5c03-4e43-a398-d442a2dabb8c" />

> >
> 
>  <img width="742" height="779" alt="스크린샷 2026-04-01 145739" src="https://github.com/user-attachments/assets/56601496-4d24-4056-830e-8e54a3d67391" />
>
> 
---

## 4. 모델링 및 성능 평가

### 모델별 성능 비교 (Base vs Final)
| 모델 | Train Score | Test Score | AUC | 비고 |
|:---|:---:|:---:|:---:|:---|
| **DecisionTree** | 0.9480 | 0.7190 | 0.5001 | 과적합(Overfitting) 발생 |
| **XGBoost** | 0.9461 | 0.8435 | 0.5072 | **최종 모델 선정** |
| **LightGBM** | 0.8751 | 0.8505 | 0.4881 | 안정적 성능 |
| **CatBoost** | 0.8668 | 0.8520 | 0.4807 | 안정적 성능|

### 최종 모델 분석 결과
* **Accuracy:** 84.35% (높은 수치 기록)
* **Recall:** 1.35% (실제 이탈자 296명 중 4명 예측)
* **결론:** 15%의 **클래스 불균형**으로 인해 모델이 다수 클래스(유지)에 편향됨. 향후 **SMOTE** 또는 **언더샘플링** 작업이 필수적.

> <img width="800" height="700" alt="572408868-dfa6a7e4-e288-4004-ac8a-73d50180e105" src="https://github.com/user-attachments/assets/226ba605-2743-42bd-b71f-ded410030cd2" />

> 
>  <img width="1000" height="500" alt="572408865-d2b07228-76f2-4b2a-bf27-2fc903f6cd76dddd" src="https://github.com/user-attachments/assets/576ec238-d6c5-4cb9-8285-ea8a00bc3d18" />
   
> 
> 
> <img width="800" height="600" alt="572408867-d4998a47-6776-4b3c-af8c-90ccd467977d" src="https://github.com/user-attachments/assets/85b54470-8901-4b95-b837-a56033eeec6d" />
> 

---

## 프로젝트 폴더 구조 (System Architecture)

전체 폴더 구조에 대한 설명입니다. 

```text
프로젝트 구조
├── main.py                    # 앱 진입점
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── models/                    # ML 파이프라인
│   ├── model_netflix.py       # 메인 실행 (Pipeline Control)
│   ├── simul_netflex.py       # 시뮬레이터 연동 스크립트
│   ├── test.py                # 테스트·실험용
│   ├── utils.py               # 공통 유틸
│   ├── model_mjk.ipynb        # 모델 실험 노트북
│   ├── Data_Preprocessing/    # 전처리
│   │   ├── load_data.py       # 데이터 로드·피처 생성
│   │   ├── cleaning.py        # 결측치 보정
│   │   ├── encoding.py        # 범주형 인코딩 등
│   │   ├── data_split.py      # 학습/검증 등 분할
│   │   ├── merge_data.py      # 데이터 병합
│   │   └── outlier_handling.py # 이상치 처리
│   ├── Modeling/              # 모델 학습·저장
│   │   ├── Model_test.py      # 알고리즘 비교 학습
│   │   ├── save_model.py      # 최적 모델 저장
│   │   └── check.py           # 검증·점검
│   ├── Display_graph/         # 시각화
│   │   ├── cm_fi_graph.py     # Confusion Matrix·피처 중요도
│   │   └── ac_ls_graph.py     # 추가 그래프
│   ├── Netflix_ML/            # 팀원별 노트북·EDA·중간 CSV·이미지
│   └── data/                  # 학습용 CSV/JSON·제출·결과·README
├── src/                       # Streamlit 대시보드·분석 UI (screens, components, design, config, utils)
├── backend/                   # Dockerfile, extract_data.py, requirements
├── data/                      # DB_QUERY_GUIDE, db_query.py, sample·server CSV, model_netflix.pkl
├── scripts/                   # CSV·시뮬레이터 샘플·검증 등 배치 스크립트
├── docs/                      # 기획·작업 이력·가이드 문서
├── catboost_info/             # CatBoost 학습 로그(실행 시 생성·추적)
└── .github/                   # 이슈 템플릿
```



### 5. 예측

#### 이탈률 비교 분석
| 구분 | 비율 (%) |
|:---|:---:|
| **실제 데이터 이탈률** | **16.29%** |
| **예측 데이터 이탈률** | **15.60%** |

> **[분석 결과]**
> 실제 이탈률과 예측치 사이의 **오차가 1% 미만**으로, 전체적인 이탈 규모를 파악하는 데 있어 모델이 매우 안정적인 성능을 보입니다. 다만, 클래스 불균형으로 인해 개별 이탈자 식별 능력(**Recall**)은 향후 고도화 작업이 필요.

---

#### 주요 피처별 이탈률 확인

**1. Tenure (가입 기간)**
* **현황:** 가입 초기(0~1개월) 유저와 초장기(61개월 이상) 유저군에서 이탈률이 상반되게 높게 나타나는 **'양극화 현상'** 발생.
* **인사이트:** 신규 유저는 서비스 적응 실패, 장기 유저는 콘텐츠 매너리즘이 주요 원인으로 판단됩니다. 가입 기간별로 차별화된 리텐션(유지) 정책이 필수적.

**2. Complain (고객 불만)**
* **현황:** 불만 사항(Complain)을 한 번이라도 접수한 고객의 이탈률이 미접수 고객 대비 **압도적으로 높음.**
* **인사이트:** 고객 불만은 이탈의 가장 강력한 선행 지표입니다. VOC(Voice of Customer) 발생 시 즉각 대응하는 **'Fast-Track'** 서비스가 이탈 방지의 핵심.

**3. CashbackAmount (혜택 체감도)**
* **현황:** 캐시백 액수가 특정 구간(100달러 단위)에 걸쳐 있는 유저들에게서 집중적인 이탈 징후 포착.
* **인사이트:** 단순히 많은 혜택을 주는 것보다 유저가 기대하는 **'혜택 문턱(Threshold)'**을 만족시키는 것이 중요합니다. 캐시백 정책과 실제 이탈 사이의 상관계수를 재점검.

---

### 6. 결론

| 위 피처들을 통한 이탈 방지 전략 제안 |
|:---|
| **1. 가입 기간별 맞춤형 케어**<br>신규 유저에게는 온보딩 콘텐츠 추천을, 장기 유저에게는 로열티 등급 및 독점 혜택을 제공하여 '락인(Lock-in)' 효과 극대화 |
| **2. 선제적 불만 관리 시스템**<br>Complain 접수 시 AI 우선순위 배정 및 즉각적인 보상(쿠폰 등)을 통해 이탈 의사를 사전에 차단하는 프로세스 구축 |
| **3. 비용 효율성 최적화**<br>'시간당 비용(Cost per Hour)'이 높은 유저를 선별하여 구독 플랜 변경 권유 및 맞춤형 프로모션을 제안하여 가격 저항감 완화 |
| **4. 데이터 품질 및 모델 고도화**<br>향후 **SMOTE 기법**을 적용하여 모델의 재현율(Recall)을 개선하고, 이상치 처리를 강화하여 예측의 정밀도를 상향 평준화함 |

### 7. Streamlit 예측 시각화
</blockquote>
<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/e907083f-c69a-477a-98d8-4066d9b8fa56" />
<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/4378d15b-9746-425e-9fc5-4250654b891e" />

---

### 8. 한계점 및 향후 개선 방향
<hr>

### 현재 한계점

- **데이터 분석 프로세스 오류**: 원본 데이터의 특성을 파악하는 EDA 전, 근거 없는 결측치 대치를 우선 진행하여 초기 데이터의 순수성과 분석 방향성 확보에 어려움을 겪음.

- **클래스 불균형(Imbalance)**: 유지(85%) 대비 이탈(15%). 모델이 다수 클래스에 편향됨에 따라 실제 이탈자를 잡아내는 재현율(Recall)이 낮게 측정됨.

- **통계적 근거 부재**: 변수의 분포나 이상치에 대한 심층적 확인 없이 전처리를 진행하여 모델 성능의 신뢰도 확보가 미흡함.

- **단순 파생 변수와 피처 선정의 한계**: 제공된 기본 피처와 단순 집계 수준의 파생 변수만으로는 이탈 여부에 영향을 미치는 결정적 패턴을 도출하기 어려웠으며, 여러 변수를 엮어내는 분석 역량 부족으로 피처 선정에 난항을 겪음.

- **초기 성능 저하 및 모델링 시도 부족**: 피처 발굴의 한계가 곧 베이스라인 모델의 성능 부진으로 이어졌고, 정작 하이퍼파라미터 튜닝이나 앙상블 등 다양하고 발전된 알고리즘을 깊게 테스트해 볼 시간적/기술적 여유가 부족했음.

### 향후 개선 방향

- **데이터 분석 순서 정립**: '원본 EDA → 결측 패턴 분석 → 통계적 근거 기반 전처리' 순으로 프로세스를 재설계하여 데이터 왜곡 최소화.
  
- **불균형 데이터 대응**: SMOTE 또는 언더샘플링 기법을 적용하여 데이터 균형을 맞춘 뒤, 정확도(Accuracy) 대신 F1-Score  핵심 지표로 설정.
  
- **정교한 피처 엔지니어링**: 단순히 기존 변수를 가공하는 것을 넘어, 유저의 '시청 주기', '장르 편식도' 등 심리적 요인을 반영한 고도화된 파생 변수와, 여러 행동들의 교차 패턴을 담아낸 복합 조건 변수 생성.

- **모델링 파이프라인 구축**: 강력한 피처를 토대로 베이스라인의 안정적인 성능을 우선적으로 확보한 후, 최신 머신러닝 모델 최적화나 딥러닝 기반 예측 모델 도입 등 다양한 모델링 기법을 여유 있게 실험해 볼 수 있는 체계 정립.
 

---
 
### 8. 한줄회고
<hr>
<blockquote>

•	김경수 :  
1. 다른 비전공자 분들하고 함께하고 싶어서 프로젝트 초반에 계획을 세운건 좋았지만 그러다 보니 전공자 분들에게 도움이 되는 프로젝트는 아니었던 것 같습니다. 
2. 머신러닝 쪽에 집중해 주셨으면 해서 제가 UI를 맞은것 까지는 좋았지만 작업 후반에는 UI 구현 쪽 일에 매몰되다 보니 팀원들을 챙기지 못했던게 아닌가 합니다. (다행히 재경님이 도와 주셔서 그나마 무사하게 넘어갔습니다. )
3. 혼자서 UI 개발을 진행하는데 코딩을 100% 할 수 있는 능력은 되지 않아서 LLM 에 많이 의존했습니다. 아예 활용을 안하는건 불가능하겠지만 개인 실력을 높히는 방향으로 사용할 수 있는 방법이 어떤게 있는지 고민해 봐야 할 것 같습니다. (ex - 작업 과정을 계획을 세우고 기록하게 해서 작업전 / 작업후에 리뷰하거나 작업된 내용이 이해되지 않으면 이해할 수 있는 방식으로 구현될 때까지 다시 개발시키고 방향을 제시하거나 등...)
4. 최대한 개발 / 모델링 시간을 확보해 드리고 싶어서 문서 작업이나 기획서 업무들을 가져와서 처리했는데 이렇게 하다보니 다른 분들이 해당 업무를 경험해볼 기회를 뺏은게 아닌가 생각이 들었습니다. 다음 번에는 팀원들이 다른 팀장님 밑에서 해당 업무들을 경험해 보셨으면 좋겠습니다. <br><br>
•	김주영 :  팀장님께서 잘 끌어주시고 머신러닝과 일주일동안 친해진 시간이어서 좋았습니다. 실행이 되는 베이스 모델을 구축했다는 점, 6개의 csv 파일에서 직접 피처 10개를 생성했다는 점, 결측치를 처리했다는 점, 클래스 불균형이 있을때에는 SMOTE 혹은 언더/오버샘플링을 해야한다는 점을 깨달았습니다. 완벽히는 못했지만 스스로 할 줄 아는 것과 모르는 것을 확실하게 알 수 있는 좋은 기회였습니다. 데이터 전처리 작업의 중요성을 알게된 값진 시간이었습니다. 이후에는 깨달은 점을 반영하여 데이터 전처리와 이상치 및 결측치 처리에 대해 좀 더 신중하고 근거있는 처리하도록 하겠습니다.<br><br>
•	문재경 :  데이터 분석 측면에서는, 도메인적인 해석 외에도 통계적이거나 기계적인 기법을 동원해 피처를 적극적으로 생성해 보고 실험을 통해 검증하는 절차가 부족했습니다. 결국 모델보다 주어진 데이터의 품질이 치명적인 것을 또다시 느꼈습니다.
팀 프로젝트 진행 측면에서는 업무 분담이 명확하게 이뤄지지 못했던 것 같습니다. 전공자 입장에서 비전공자 팀원들에게 방향을 명확히 설명하지 못하고 '일단 부딪혀 보자'고 했던 것이 결국 병목 현상으로 되돌아왔습니다. 차기 프로젝트에서는 시작 단계부터 제가 더 많은 품을 들이더라도, 각자가 확실히 해낼 수 있는 부분을 파악해서 모두가 이해할 수 있는 방향으로의 노력이 필요하겠다는 생각이 들었습니다.<br><br>
•	이성진 :  모델의 성능은 알고리즘보다 데이터의 균형과 상태에 더 큰 영향을 받는다는 점을 배웠습니다. 
특히 타겟 데이터의 비율이 맞지 않는 클래스 불균형 상황에서는 아무리 뛰어난 모델이라도 소수 샘플의 패턴을 학습하지 못해 AUC 점수 개선에 한계가 있음을 확인했습니다. 그리고 EDA를 통해 컬럼의 특성을 이해하고 이를 어떻게 조합할지 고민하며, 데이터 비율을 사전에 점검하는 과정이 모델 향상에 중요한 역할이라는 것을 알게 되었습니다<br><br>
•	이재강 :  데이터 분석과 시각화를 통해 전처리의 중요성을 체감하며, 머신러닝과 딥러닝을 실제 데이터에 직접 적용해 볼 수 있었던 유익한 시간이었습니다. 특히 타겟 불균형을 해결할 오버/언더샘플링의 필요성을 뒤늦게 알게 된 점은 아쉬움이 남지만, 그만큼 모델 성능을 높이는 핵심 포인트를 확실히 배울 수 있었습니다.<br><br>
•	이재건 :  다른(넷플릭스) 데이터로 딥러닝을 해보았는데 다른 모델보다 간단하게 테스트를 할 수 있는 것이 신기하였고
EDA를 통해서 연관성이 있는 컬럼을 구해보는 것도 어떤 것이 연관이 있고 없는지의 차이점을 알 수 있는 시간이었고
두 번째 프로젝트를 하면서 친분이 더 돈독해지는 시간이어서 너무 좋았습니다.<br><br>


</blockquote>
---

