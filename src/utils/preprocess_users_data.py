import os
import pandas as pd
import numpy as np

def preprocess_users_data(users_df: pd.DataFrame) -> pd.DataFrame:
    """유저 데이터 전처리 함수
    모델링 노트북의 처리를 바탕으로 인코딩 직전까지의 상태로 만듭니다.
    """
    # 원본 데이터프레임 복사
    df = users_df.copy()
    
    # 1. 타겟 변수 생성 및 불필요 컬럼 제거
    if 'is_active' in df.columns:
        df['churned'] = 1 - df['is_active']
    
    drop_cols = ['is_active', 'user_id', 'email', 'first_name', 'last_name', 'city', 'created_at']
    # 존재하는 컬럼만 삭제
    drop_cols = [col for col in drop_cols if col in df.columns]
    df = df.drop(columns=drop_cols)
    
    # 2. 나이(age) 이상치 처리
    if 'age' in df.columns:
        age_mean = df['age'].mean()
        age_std = df['age'].std()
        df = df[(df['age'] >= age_mean - 2 * age_std) & (df['age'] <= age_mean + 2 * age_std)]
        
    # 3. 성별(gender) 변수 범주화
    if 'gender' in df.columns:
        def proc_gender(x):
            if x in ['Male', 'Female']:
                return x
            else:
                return 'Other'
        df['gender'] = df['gender'].map(proc_gender)
        
    # 4. 월별 지출(monthly_spend) 결측치 처리 및 파생 변수 생성
    if 'monthly_spend' in df.columns and 'subscription_plan' in df.columns:
        plan_spend_mean = df.groupby('subscription_plan')['monthly_spend'].mean()
        df['monthly_spend'] = df['monthly_spend'].fillna(df['subscription_plan'].map(plan_spend_mean))
        df['monthly_spend_log'] = np.log1p(df['monthly_spend'])
        
    # 5. 가구원 수(household_size) 결측치 처리 및 파생 변수 생성
    if 'household_size' in df.columns:
        df['household_size_missing'] = df['household_size'].isna().astype(int)
        df['household_size'] = df['household_size'].fillna(0)
        
    # 6. 구독 시작일(subscription_start_date) 분리
    if 'subscription_start_date' in df.columns:
        df['subscription_start_date'] = pd.to_datetime(df['subscription_start_date'])
        df['start_year'] = df['subscription_start_date'].dt.year
        df['start_month'] = df['subscription_start_date'].dt.month
        df['start_day'] = df['subscription_start_date'].dt.day
        df['start_weekday'] = df['subscription_start_date'].dt.weekday
        df = df.drop(columns=['subscription_start_date'])
        
    # 7. 전처리된 데이터 저장
    save_dir = os.path.join('data', 'sample')
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, 'preprocessed_users.csv')
    df.to_csv(save_path, index=False)
    
    return df
