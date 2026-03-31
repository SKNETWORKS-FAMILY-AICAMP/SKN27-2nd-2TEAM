import pandas as pd
import numpy as np
import os

def verify_refine_logic():
    # 데이터가 위치한 실제 경로
    base_path = r'C:\dev\project\SKN27-2nd-2TEAM\models\data'
    
    print(f"--- 검증 시작 (작업 경로: {base_path}) ---")

    try:
        # 1. 파일 로드
        users = pd.read_csv(os.path.join(base_path, 'users.csv'))
        watch = pd.read_csv(os.path.join(base_path, 'watch_history.csv'))
        search = pd.read_csv(os.path.join(base_path, 'search_logs.csv'))
        recommend = pd.read_csv(os.path.join(base_path, 'recommendation_logs.csv'))
        print("✔ 1. 모든 원본 데이터 로드 성공")

        # 2. 계정 생성 개월수 계산 (account_age_months)
        users['subscription_start_date'] = pd.to_datetime(users['subscription_start_date'])
        ref_date = users['subscription_start_date'].max()
        users['account_age_months'] = ((ref_date.year - users['subscription_start_date'].dt.year) * 12 + 
                                       (ref_date.month - users['subscription_start_date'].dt.month))
        print("✔ 2. 계정 생성 개월수 계산 완료")

        # 3. 사용 기기 수 계산 (devices_used)
        combined_logs = pd.concat([
            watch[['user_id', 'device_type']],
            search[['user_id', 'device_type']],
            recommend[['user_id', 'device_type']]
        ]).drop_duplicates()
        
        device_counts = combined_logs.groupby('user_id')['device_type'].nunique().reset_index()
        device_counts.columns = ['user_id', 'devices_used']
        print("✔ 3. 로그 기반 기기 이용 수 집계 완료")

        # 4. 컬럼명 매핑 및 정제
        mapping = {
            'age': 'age',
            'gender': 'gender',
            'country': 'country',
            'subscription_plan': 'subscription_type',
            'monthly_spend': 'monthly_fee',
            'primary_device': 'primary_device'
        }
        
        refined = users[['user_id', 'age', 'gender', 'country', 'subscription_plan', 'monthly_spend', 'primary_device', 'account_age_months']].copy()
        refined = refined.rename(columns=mapping)

        # 5. 데이터 병합 및 결측치 처리
        final_df = pd.merge(refined, device_counts, on='user_id', how='left')
        final_df['devices_used'] = final_df['devices_used'].fillna(1).astype(int)
        print("✔ 4. 데이터 병합 및 최종 정제 완료")

        # 6. 최종 8개 컬럼 선택
        cols = ['age', 'gender', 'country', 'account_age_months', 'subscription_type', 'monthly_fee', 'primary_device', 'devices_used']
        check_output = final_df[cols]

        # --- 출력 확인 (저장 없이 결과만 출력) ---
        print("\n" + "="*50)
        print(" 정제 결과 미리보기 (상위 5행)")
        print("="*50)
        print(check_output.head())
        
        print("\n" + "="*50)
        print(" 데이터 요약 정보 (Info)")
        print("="*50)
        print(check_output.info())
        
        print("\n✔ 모든 로직이 정상적으로 실행되었습니다. (파일 저장은 수행되지 않음)")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == "__main__":
    verify_refine_logic()