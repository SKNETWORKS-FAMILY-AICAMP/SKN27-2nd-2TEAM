# Netflix 이탈 데이터 분석 정리

## 문서 목적

공통적으로 분석은 아래 질문에 답하기 위해 진행

- **언제 이탈이 증가했는가**
- **11월 이탈 증가가 어떤 사용자층에서 나타났는가**
- **11월 이탈 증가와 함께 어떤 행동 변화가 관찰되는가**
- **상위 요금제 유저의 churn은 어떤 특징을 보이는가**


---

## 분석 기준 요약

### 1. 추정 churn date
실제 탈퇴일이 없기 때문에, non-churn 유저의 복귀 gap을 기준으로 churn 유저의 추정 churn date를 만듦

- non-churn 유저의 복귀 gap 분포를 확인
- median(50%) 복귀 시점인 **38일**을 기준으로
- 마지막 핵심 활동일(`last_core_activity_date`)에 gap을 더해 `estimated_churn_date`를 생성
- 이후 `final_estimated_churn_date`로 보정 및 사용

### 2. 비교 구간
주요 비교는 다음 기준을 사용함

- **Base** = 2025-09 ~ 2025-10 estimated churn 유저
- **Target** = 2025-11 estimated churn 유저

이 기준을 택한 이유는, 월별 증가율 그래프에서 **11월 증가가 가장 해석 가치가 높았고**, 12월은 관측 종료일 보정(capping) 영향이 섞여 있어 직접 비교 기준으로는 적절하지 않았기 때문

### 3. 주의점
- `monthly_spend`는 구독형 서비스의 고정 요금처럼 보이지 않으므로, **플랜 월요금**이 아니라 **유저별 월 지출/가치 지표**로 해석하는 것이 안전
- 11월 탈퇴자 vs 11월 이후 잔존자 비교에서, **11월 행동만 사용한 비교는 상태 진단에는 유효하지만 원인 분석으로는 약함.**  
  같은 달에 이미 이탈한 사람은 행동량이 거의 0으로 수렴하기 쉽기 때문

---

# 1. review/recommendation date 영향 확인 그래프
![review/recommendation 영향 확인 그래프](image\output.png)
## 그래프를 그린 이유
- `review_date`와 `recommendation_click_date` 같은 날짜 컬럼이 churn 판단에 실제로 큰 영향을 주는지 확인하기 위해
- 마지막 활동일 정의에 어떤 날짜를 포함해야 할지 결정하기 위해

## 해석
- review와 recommendation click 날짜를 마지막 활동 정의에 포함해도 **변화되는 비율이 작음**
- 따라서 두 날짜는 churn date 추정에서 **핵심 기준으로 보기 어려움**
- 이후 핵심 활동일은 `watch_date`, `search_date` 중심으로 잡는 것이 더 타당하다고 판단함

## 정리 문장
> review와 recommendation click 날짜를 포함해도 churn 판단 변화 비율이 크지 않아, 마지막 핵심 활동일 정의에서는 watch와 search를 중심으로 두는 것이 적절하다고 판단함

---

# 2. non-churn return gap 분포 그래프
![review/recommendation 영향 확인 그래프](image\output2.png)
![review/recommendation 영향 확인 그래프](image\output3.png)
### 📊 데이터 통계 요약 (Metric Summary)

| Metric | Value |
| :--- | ---: |
| **Count** | 97,012.00 |
| **Mean** | 53.91 |
| **Median** | 38.00 |
| **P75** | 75.00 |
| **P90** | 124.00 |
| **P95** | 161.00 |
| **P99** | 245.00 |
| **Max** | 537.00 |
## 그래프를 그린 이유
- churn 유저의 실제 탈퇴일이 없기 때문에, non-churn 유저의 복귀 패턴을 기준으로 **추정 churn date**를 만들기 위해
- “마지막 활동 후 어느 정도 지나면 사실상 이탈로 볼 수 있는가”에 대한 기준을 정하기 위해

## 해석
- non-churn 유저의 복귀 gap을 보니, **median(50%) 기준 38일 이내 복귀**가 확인
- 따라서 churn 유저는 마지막 핵심 활동일에 **38일을 더한 날짜**를 1차 추정 churn date로 사용할 수 있다고 봄
- 이 그래프는 churn date 자체를 예측하는 그래프가 아니라, **추정 기준을 정하는 근거 그래프**

## 정리 문장
> non-churn 유저의 복귀 gap 분포에서 median이 38일로 확인되어, churn 유저의 추정 churn date는 마지막 핵심 활동일에 38일을 더하는 방식으로 정의

---

# 3. 월별 estimated churn user 수 그래프
![review/recommendation 영향 확인 그래프](image\output4.png)
## 그래프를 그린 이유
- 추정 churn date 기준으로 **월별 이탈 규모가 어떻게 변하는지** 보기 위해
- 어떤 달부터 churn 증가가 본격화되었는지 확인하기 위해
- 이후 비교 기준 달을 정하기 위해

## 해석
- 월별 estimated churn user 수는 전반적으로 증가하는 흐름을 보임
- 특히 **11월 증가가 해석 가치가 높았고**, 12월은 cap 처리로 값이 겹치는 영향이 있어 직접 해석 대상에서 제외하는 것이 적절
- 따라서 본 분석의 주요 비교 기준은 **9~10월 vs 11월**로 설정

## 정리 문장
> estimated churn user 수는 월별로 증가했으며, 12월은 보정 영향이 크므로 11월을 핵심 비교 달로 두고 9~10월과 비교하는 것이 가장 적절하다고 판단

---

# 4. 월별 churn 증가율(증감) 그래프
![review/recommendation 영향 확인 그래프](image\output5.png)
## 그래프를 그린 이유
- 단순 user 수가 아니라, **전월 대비 얼마나 증가했는지**를 보기 위해
- 11월이 정말 “증가가 두드러진 달”인지 정량적으로 확인하기 위해

## 해석
- 증가율 기준으로 보면 **8월과 11월**에 상승이 관찰됨
- 다만 8월은 직전 월 데이터가 적어 비교 안정성이 낮았고,
- 11월은 더 직접적으로 비교 가능한 구간이라 **9~10월 vs 11월** 구조가 타당하다고 봄

## 정리 문장
> 월별 증가율을 확인한 결과 11월은 전월 대비 churn 증가가 의미 있게 나타난 구간으로 보였으며, 비교 기준으로 설정하기에 적절

---

# 5. 세그먼트 구성 비교 그래프

## 공통 목적
- 11월 churn 증가가 **어떤 사용자층에서 상대적으로 더 많이 나타났는지** 확인하기 위해
- 특정 세그먼트의 비중 변화가 있는지 보기 위해

---

## 5-1. 구독 플랜(subscription_plan) 구성 비교
![review/recommendation 영향 확인 그래프](image\output6.png)
### 그래프를 그린 이유
- 11월 churn 증가가 특정 요금제 사용자에서 상대적으로 더 크게 나타났는지 보기 위해

### 해석
- **Target(11월)** 에서 `Premium`, `Standard` 비중이 더 높음
- 반대로 `Basic`, `Premium+` 비중은 상대적으로 낮음
- 즉 11월 churn 증가는 극단 플랜보다는 **주력 구독층(Standard, Premium)** 에서 더 크게 나타난 것으로 해석

### 정리 문장
> 11월 churn 증가는 Premium과 Standard 사용자 비중 확대로 나타나, 주력 구독층 중심의 이탈 증가로 해석할 수 있음

---

## 5-2. 주 사용 디바이스(primary_device) 구성 비교
![review/recommendation 영향 확인 그래프](image\output7.png)
### 그래프를 그린 이유
- 11월 churn 증가가 어떤 사용 환경에서 더 많이 나타났는지 보기 위해

### 해석
- **Desktop 비중이 Target(11월)에서 증가**
- 11월 churn 증가는 개인용 디바이스 중심, 특히 **Desktop 사용자 증가**와 연결된 것으로 볼 수 있음

### 정리 문장
> 11월 churn 증가는 Desktop 사용자 비중 확대와 함께 나타나, 개인용 디바이스 중심 사용자층에서 상대적으로 더 크게 발생한 것으로 해석할 수 있음

---

## 5-3. 국가(country) 구성 비교
![review/recommendation 영향 확인 그래프](image\output8.png)
### 그래프를 그린 이유
- 특정 국가 사용자층에서 churn 증가가 더 두드러졌는지 확인하기 위해

### 해석
- 전체 데이터에서도 `USA` 비중이 크고, 11월 churn 증가 구간에서도 USA 비중이 상대적으로 높게 나타남
- 따라서 미국 사용자군이 churn 증가 해석에서 핵심 기준 국가로 볼 수 있음

### 정리 문장
> 국가 기준으로는 미국(USA) 사용자의 비중이 높고 11월 이탈 증가에서도 중심축으로 나타나, 주요 해석 대상 국가로 보는 것이 적절

---

## 5-4. 연령대(age_group) 구성 비교
![review/recommendation 영향 확인 그래프](image\output9.png)
### 그래프를 그린 이유
- churn 증가가 특정 연령대에서 상대적으로 더 크게 나타났는지 보기 위해

### 해석
- 연령대별 큰 차이는 보이지 않음
- 일부 구간에서 30대, 40~50대 차이가 약하게 보였지만, 전체 설명력은 상대적으로 낮음

### 정리 문장
> 연령대별 구성 차이는 존재하지만, 플랜이나 디바이스 수준만큼 강한 설명 변수로 보긴 어려움

---

# 6. 행동 지표 분포 비교 그래프 (9~10월 churn vs 11월 churn)

## 그래프를 그린 이유
- 단순히 “누가 많이 빠졌는가”가 아니라,  
  **11월 churn 유저의 행동 패턴이 실제로 나빠졌는지** 확인하기 위해
- 평균값만 보면 왜곡될 수 있으므로, **boxplot으로 분포 전체**를 보려고 함

비교 컬럼:
- `completion_rate`
- `avg_watch_time_minutes`
- `recommendation_click_rate`
- `content_interactions`
- `rating_given`

---

## 6-1. completion_rate
![review/recommendation 영향 확인 그래프](image\output10.png)
### 해석
- 11월(Target) box가 Base보다 아래로 내려가 있지 않았음
- 중앙값도 비슷하거나 약간 더 높음
- 따라서 **완료율 저하가 11월 churn 증가의 핵심 요인이라고 보긴 어려움**

### 정리 문장
> completion_rate는 11월 churn 유저에서 뚜렷하게 낮아지지 않아, 11월 churn 증가를 설명하는 핵심 요인으로 보긴 어려움.

---

## 6-2. avg_watch_time_minutes
![review/recommendation 영향 확인 그래프](image\output11.png)
### 해석
- 11월(Target) box가 약간 위쪽에 위치했고 중앙값도 조금 더 높음
- 즉 11월 churn 유저는 **시청시간이 줄었다기보다 유지되거나 일부는 더 높은 패턴**을 보임
- 따라서 churn 증가는 단순한 사용량 감소로만 해석하기 어려움

### 정리 문장
> avg_watch_time_minutes는 11월 churn 유저에서 오히려 유지되거나 다소 높은 패턴을 보여, churn 증가가 단순 시청시간 감소로 설명되지는 않음.

---

## 6-3. recommendation_click_rate
![review/recommendation 영향 확인 그래프](image\output12.png)
### 해석
- 11월(Target) box가 Base보다 약간 아래에 위치함
- 중앙값과 상단 범위도 소폭 낮음
- 이 지표는 5개 중 **가장 직접적인 악화 신호**로 보였음

### 정리 문장
> recommendation_click_rate는 11월 churn 유저에서 소폭 낮아져, 추천 기반 탐색 반응성이 약화된 패턴을 보였음.

---

## 6-4. content_interactions
![review/recommendation 영향 확인 그래프](image\output13.png)
### 해석
- 중앙값은 거의 비슷했고, 11월(Target)은 일부 상단 구간이 오히려 더 큼
- 즉 전반적 참여도 저하를 강하게 주장하기엔 부족하고, **비슷하거나 일부는 더 활발한 구간**도 있었음

### 정리 문장
> content_interactions는 9~10월과 큰 차이를 보이지 않았고, 일부 구간에서는 오히려 더 높은 값도 관찰되어 참여도 저하를 핵심 요인으로 단정하긴 어려움.

---

## 6-5. rating_given
![review/recommendation 영향 확인 그래프](image\output14.png)
### 해석
- 중앙값은 유사했지만, 11월(Target) 하단 구간이 조금 더 아래로 내려감
- 즉 전체적으로 큰 만족도 저하라기보다는, **일부 낮은 평점 사용자군이 더 포함된 패턴**으로 해석하는 것이 적절

### 정리 문장
> rating_given은 중심 분포는 유사했지만 11월 churn 유저에서 낮은 평점 구간이 일부 확대되어, 부분적 만족도 저하 신호가 관찰됨.

---

## 행동 지표 1차 종합 해석
> 11월 churn 유저는 추천 클릭률은 다소 낮아졌지만, 완료율과 평균 시청시간은 유지되거나 오히려 높은 패턴을 보였다. 따라서 11월 churn 증가는 단순한 사용량 감소보다는 추천 기반 탐색 반응성 저하와 일부 만족도 약화가 함께 나타난 현상으로 보는 것이 더 타당함.

---

# 7. 추가 행동 지표 분포 비교 그래프

비교 컬럼:
- `review_helpfulness_ratio`
- `binge_day_ratio`
- `avg_search_duration_seconds`

## 그래프를 그린 이유
- 1차 행동 지표 외에, **리뷰 반응의 질 / 몰아보기 성향 / 탐색 마찰** 같은 추가 신호가 있는지 보기 위해

---

## 7-1. avg_search_duration_seconds
![review/recommendation 영향 확인 그래프](image\output15.png)
### 해석
- 11월(Target) box가 Base보다 약간 위에 위치했고 중앙값도 조금 높았다
- 이는 11월 churn 유저가 **검색 과정에서 조금 더 오래 머무른 경향**, 즉 탐색 마찰이 약간 커졌을 가능성을 시사함
- 다만 차이는 크지 않아 **보조 신호**로 보는 것이 적절

### 정리 문장
> avg_search_duration_seconds는 11월 churn 유저에서 소폭 높게 나타나, 콘텐츠 탐색 과정의 마찰 가능성을 일부 시사했다. 다만 핵심 단일 요인으로 보기는 어려움.

---

## 7-2. binge_day_ratio
![review/recommendation 영향 확인 그래프](image\output16.png)
### 해석
- Base와 Target 모두 대부분 0 근처에 몰려 있음
- 일부 outlier는 있었지만, 전체 집단 차이를 설명할 수준은 아니였음

### 정리 문장
> binge_day_ratio는 대부분의 유저가 0에 가까워, 11월 churn 증가를 설명하는 핵심 변수로 보긴 어려움.

---

## 7-3. review_helpfulness_ratio
![review/recommendation 영향 확인 그래프](image\output17.png)
### 해석
- Base와 Target의 박스 모양이 거의 동일했고 중앙값도 유사함
- 리뷰가 얼마나 유용하게 받아들여졌는지는 11월 churn 증가와 직접적으로 연결되는 신호로 보기 어려움

### 정리 문장
> review_helpfulness_ratio는 Base와 Target 간 분포 차이가 거의 없어, 리뷰 반응의 질 자체는 11월 churn 증가를 직접적으로 설명하는 핵심 요인으로 보기 어려움.

---

## 추가 행동 지표 종합 해석
> 추가 행동 지표 중에서는 `avg_search_duration_seconds`만 11월 churn 유저에서 약간 높아져 탐색 마찰 가능성을 시사했고, `binge_day_ratio`와 `review_helpfulness_ratio`는 설명력이 낮은 보조 지표로 판단.

---

# 8. 11월 churn 유저 내 High tier vs Low tier 비교 그래프

## 비교 정의
- **High tier** = `Premium`, `Premium+`
- **Low tier** = `Basic`, `Standard`

## 그래프를 그린 이유
- `monthly_spend`가 플랜 요금처럼 보이지 않아 고저가 사용자를 정의하기 어렵다고 판단했기 때문에,
- 구독형 서비스 구조에 맞춰 **상위 요금제 churn 유저**와 **하위 요금제 churn 유저**의 차이를 보기 위해

비교 컬럼:
- `recommendation_click_rate`
- `rating_given`
- `content_interactions`

---

## 8-1. recommendation_click_rate
![review/recommendation 영향 확인 그래프](image\output18.png)
### 해석
- High tier box가 Low tier보다 아래에 위치했다
- 즉 상위 요금제 churn 유저는 하위 요금제 churn 유저보다 **추천에 덜 반응하는 경향**을 보임

### 정리 문장
> High tier churn 유저는 Low tier churn 유저보다 recommendation_click_rate 분포가 더 낮아, 추천 기반 탐색 반응성이 더 약한 상태에서 churn한 것으로 해석할 수 있음.

---

## 8-2. rating_given
![review/recommendation 영향 확인 그래프](image\output19.png)
### 해석
- High tier box가 Low tier보다 위쪽에 위치함
- 중앙값도 High tier가 더 높음
- 즉 상위 요금제 churn 유저는 **콘텐츠 만족도 자체는 더 낮지 않다. 오히려 더 높은 편**이었음

### 정리 문장
> High tier churn 유저는 Low tier churn 유저보다 rating_given 분포가 더 높게 나타나, 상위 요금제 churn은 콘텐츠 불만보다 추천 반응성 저하와 더 관련 있을 가능성을 시사함.

---

## 8-3. content_interactions
![review/recommendation 영향 확인 그래프](image\output20.png)
### 해석
- High tier box가 Low tier보다 약간 위에 위치함
- 즉 상위 요금제 churn 유저는 추천 클릭률은 낮았지만, **전체 상호작용은 더 낮지 않았고 오히려 약간 높음**

### 정리 문장
> High tier churn 유저는 content_interactions 분포가 더 낮지 않았고, 오히려 소폭 높게 나타났다. 이는 상위 요금제 유저가 플랫폼 내 활동은 유지하면서도 추천 반응성은 약화된 상태에서 churn했을 가능성을 시사함.

---

## High/Low tier 종합 해석
> High tier churn 유저는 Low tier churn 유저보다 추천에는 덜 반응했지만, 상호작용은 유지되고 콘텐츠 만족도는 더 높았다. 따라서 상위 요금제 churn은 전반적 사용 저하나 콘텐츠 불만보다 **추천 기반 탐색 반응성 약화**와 더 밀접한 패턴으로 해석할 수 있음.

---


---

# 9. 상관관계 히트맵

## 그래프를 그린 이유
- 기본 user 정보와 파생 행동 지표를 모두 포함했을 때,
- 변수들 사이에 **어떤 상관관계가 있는지** 확인하기 위해
- 향후 모델링 시 다중공선성 또는 유사 정보 중복 가능성을 보기 위해

## 해석
- 이 그래프는 개별 변수의 churn 설명력보다, **변수끼리의 관계 구조**를 보는 용도
- 일반적으로는 사용량/참여도 지표끼리 양의 상관이 나타나고, 날짜/식별자/문자열 컬럼은 제외하는 방향이 적절
- 히트맵은 최종 예측 변수 선정 전, **중복 정보 정리**를 위한 참고 자료로 활용

---

# 최종 종합 결론

## 1. 11월 churn 증가 자체
- 11월은 9~10월 대비 estimated churn 증가가 해석 가치가 높은 구간임
- 따라서 9~10월 vs 11월 비교는 타당

## 2. 세그먼트 측면
- 11월 churn 증가는 주력 구독층(Standard, Premium), Desktop 사용자, 미국 사용자 중심으로 상대적으로 더 크게 나타남
- 연령대는 보조적 신호 수준

## 3. 행동 측면
- 11월 churn 증가에서 가장 직접적으로 약화된 신호는 **recommendation_click_rate**
- `content_interactions`, `rating_given`은 큰 폭의 악화보다는 부분적 또는 약한 변화
- `completion_rate`, `avg_watch_time_minutes`는 오히려 유지되거나 더 높아, 단순 사용량 감소만으로는 설명되지 않았음
- 추가 지표 중에는 `avg_search_duration_seconds`만 보조 신호로 의미가 있었고, `binge_day_ratio`, `review_helpfulness_ratio`는 설명력이 낮음

## 4. 상위 요금제 churn 해석
- High tier churn 유저는 추천에는 덜 반응했지만, 콘텐츠 만족도는 더 높고 상호작용도 유지됨
- 따라서 상위 요금제 churn은 콘텐츠 불만보다 **추천 기반 탐색 반응성 약화**와 더 관련 있는 패턴으로 보임


---

# 한 문장 요약
> 11월 estimated churn 증가는 주력 구독층과 Desktop·USA 사용자에서 상대적으로 더 크게 나타났고, 행동 측면에서는 추천 기반 탐색 반응성 저하가 가장 직접적인 신호로 관찰되었다. 특히 상위 요금제 churn 유저는 콘텐츠 만족도는 유지하면서도 추천 반응성은 약화된 패턴을 보여, churn 증가를 단순한 사용량 감소보다 플랫폼 반응성 저하와 연결해 해석하는 것이 더 타당하다.
