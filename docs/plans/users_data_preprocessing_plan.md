# users 데이터 전처리 파이프라인 계획

`src/utils/preprocess_users_data.py` 파일의 `preprocess_users_data` 함수에 다음 순서대로 전처리 로직을 구현합니다. 모델링 노트북의 처리를 바탕으로 인코딩 직전까지의 상태로 만듭니다.

1. **타겟 변수 생성 및 불필요 컬럼 제거**
  - `churned` 파생 변수 생성: `1 - is_active`
  - 분석에 불필요한 컬럼 제거: `['is_active', 'user_id', 'email', 'first_name', 'last_name', 'city', 'created_at']`
2. **나이(age) 이상치 처리**
  - `age` 컬럼의 평균과 표준편차를 계산하여 `평균 ± 2 * 표준편차` 범위를 벗어나는 데이터(행) 제거
3. **성별(gender) 변수 범주화**
  - `Male`, `Female` 이외의 값(결측치 포함)은 모두 `'Other'`로 변환
4. **월별 지출(monthly_spend) 결측치 처리 및 파생 변수 생성**
  - `subscription_plan` 그룹별 `monthly_spend` 평균값을 계산하여 결측치 대치
  - 로그 변환된 파생 변수 `monthly_spend_log` 추가 (`np.log1p` 활용)
5. **가구원 수(household_size) 결측치 처리 및 파생 변수 생성**
  - 결측치 여부를 나타내는 `household_size_missing` 컬럼 추가 (결측 시 1, 아니면 0)
  - `household_size`의 결측치는 0으로 대치
6. **구독 시작일(subscription_start_date) 분리**
  - `datetime` 타입으로 변환 후 연도(`start_year`), 월(`start_month`), 일(`start_day`), 요일(`start_weekday`) 컬럼 추가
  - 기존 `subscription_start_date` 컬럼 제거
7. **전처리된 데이터 저장**
  - 다른 곳에서 확인할 수 있도록, 반환하기 전 처리된 데이터프레임을 `data/sample/` 디렉토리에 CSV 파일(예: `preprocessed_users.csv`)로 저장합니다. 
  - 저장 시 `data/sample` 디렉토리가 존재하지 않는다면 자동으로 생성되도록 처리합니다.

**참고사항:** 

- 원-핫 인코딩(`get_dummies`) 및 오디널 인코딩(`OrdinalEncoder`) 등의 작업은 제외됩니다. 
- 주어진 `users_df` 데이터프레임을 원본 그대로 수정하기보다는 복사본(`copy()`)을 생성해 처리한 후 반환하는 방식을 권장합니다.