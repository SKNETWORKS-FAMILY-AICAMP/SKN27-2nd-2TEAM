import pandas as pd
from IPython.display import display

# ─────────────────────────────────────────
# 1. 데이터 기본 정보 확인
# ─────────────────────────────────────────
def check_data_info(Netflix: pd.DataFrame) -> None:
    """데이터 크기, 상위 행, 컬럼 정보 출력"""
    print(f"데이터셋 모양: {Netflix.shape}")
    display(Netflix.head())
    Netflix.info()


# ─────────────────────────────────────────
# 2. 불필요한 컬럼 제거
# ─────────────────────────────────────────
def drop_columns(train: pd.DataFrame, test: pd.DataFrame, ori_te: pd.DataFrame) -> pd.Series:
    """제출용 user_id 저장 후 불필요한 컬럼 제거"""

    # 제출용 user_id 저장 (매우 중요!)
    test_user_id = test['user_id'].copy()

    print(f'before: {train.shape} / {test.shape}')

    drop_cols = ['user_id', 'email', 'first_name', 'last_name',
                'created_at', 'country', 'state_province', 'city']

    for df in [train, test, ori_te]:
        df.drop(columns=drop_cols, axis=1, inplace=True)

    print(f'after: {train.shape} / {test.shape}')
    train.info()

    return test_user_id


# ─────────────────────────────────────────
# 3. 결측치 처리
# ─────────────────────────────────────────
def get_age_group(age) -> str:
    """나이 → 연령대 변환"""
    if pd.isna(age) : return 'Unknown'
    if age < 20     : return '10s'
    elif age < 40   : return '20-30s'
    elif age < 60   : return '40-50s'
    else            : return '60s+'


def fill_missing_values(train: pd.DataFrame, test: pd.DataFrame, ori_te: pd.DataFrame) -> None:
    """결측치 처리 (age, gender, monthly_spend, household_size)"""

    # 처리 전 결측치 현황
    print('=== 처리 전 결측치 현황 ===')
    print(f'train: {train.isnull().sum().sum()}')
    print(f'test : {test.isnull().sum().sum()}')
    print(f'ori_te: {ori_te.isnull().sum().sum()}')

    # 1. age, gender 처리
    age_median  = train['age'].median()
    gender_mode = train['gender'].mode()[0]

    for df in [train, test, ori_te]:
        df['age']    = df['age'].fillna(age_median)
        df['gender'] = df['gender'].fillna(gender_mode)

    # 2. 연령대 임시 컬럼 생성
    for df in [train, test, ori_te]:
        df['age_group'] = df['age'].apply(get_age_group)

    # 3. 10대 monthly_spend 결측치 → 0
    for df in [train, test, ori_te]:
        df.loc[(df['age_group'] == '10s') & (df['monthly_spend'].isna()), 'monthly_spend'] = 0

    # 4. 수치형 컬럼 연령대별 중앙값으로 채우기
    fill_cols = ['monthly_spend', 'household_size']

    for col in fill_cols:
        medians        = train.groupby('age_group')[col].median()
        overall_median = train[col].median()

        for df in [train, test, ori_te]:
            df[col] = df[col].fillna(df['age_group'].map(medians))
            df[col] = df[col].fillna(overall_median)

    # 5. 임시 컬럼 삭제
    for df in [train, test, ori_te]:
        actual_drop = [c for c in ['age_group'] if c in df.columns]
        df.drop(columns=actual_drop, inplace=True)

    # 처리 후 결측치 현황
    print('=== 처리 후 결측치 현황 ===')
    print(f'train: {train.isnull().sum().sum()}')
    print(f'test : {test.isnull().sum().sum()}')
    print(f'ori_te: {ori_te.isnull().sum().sum()}')