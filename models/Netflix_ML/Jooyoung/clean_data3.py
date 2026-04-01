import pandas as pd
import numpy as np
import os

def verify_refine_logic():
    base_path = 'C:\dev\project\SKN27-2nd-2TEAM\models\data'
    
    print(f"--- 데이터 정제 및 10개 컬럼 통합 생성 시작 ---")

    try:
        # 1. 원본 파일 로드
        users = pd.read_csv(os.path.join(base_path, 'users.csv'))
        watch = pd.read_csv(os.path.join(base_path, 'watch_history.csv'))
        search = pd.read_csv(os.path.join(base_path, 'search_logs.csv'))
        recommend = pd.read_csv(os.path.join(base_path, 'recommendation_logs.csv'))
        print("✔ 1. 모든 원본 데이터 로드 성공")

        # ---------------------------------------------------------
        # [카테고리 2] 계산 및 가공 컬럼 생성
        # ---------------------------------------------------------
        # 2-1. 계정_생성_개월수 (account_age_months)
        users['subscription_start_date'] = pd.to_datetime(users['subscription_start_date'])
        ref_date = users['subscription_start_date'].max() 
        users['account_age_months'] = ((ref_date.year - users['subscription_start_date'].dt.year) * 12 + 
                                       (ref_date.month - users['subscription_start_date'].dt.month))

        # 2-2. 사용_기기_수 (devices_used)
        combined_logs = pd.concat([
            watch[['user_id', 'device_type']],
            search[['user_id', 'device_type']],
            recommend[['user_id', 'device_type']]
        ]).drop_duplicates()
        device_counts = combined_logs.groupby('user_id')['device_type'].nunique().reset_index()
        device_counts.columns = ['user_id', 'devices_used']
        print("✔ 2. 가공 컬럼(개월수, 기기수) 생성 완료")

        # ---------------------------------------------------------
        # [카테고리 3] 파생 변수 생성 기초 데이터 집계
        # ---------------------------------------------------------
        watch_stats = watch.groupby('user_id').agg(
            avg_progress=('progress_percentage', 'mean'),
            total_watch_minutes=('watch_duration_minutes', 'sum'),
            completed_count=('action', lambda x: (x == 'completed').sum()),
            total_count=('action', 'count')
        ).reset_index()
        
        # 3-1. 완독률 (Completion Rate) 공식 적용
        watch_stats['completion_rate'] = (watch_stats['avg_progress'] / 100) + (watch_stats['completed_count'] / watch_stats['total_count'])
        print("✔ 3. 파생 변수(완독률) 계산 완료")

        # ---------------------------------------------------------
        # 데이터 통합 (Merge)
        # ---------------------------------------------------------
        final_df = users.copy()
        final_df = pd.merge(final_df, device_counts, on='user_id', how='left')
        final_df = pd.merge(final_df, watch_stats, on='user_id', how='left')

        # ---------------------------------------------------------
        # [카테고리 3] 파생 변수 - 시간당 비용 계산
        # ---------------------------------------------------------
        # 3-2. 시간당 비용 (Cost per Hour): 월 지출액 / (총 시청 시간 / 60)
        # 분모가 0이 되는 것을 방지하기 위해 0.1분(보정값) 사용
        final_df['cost_per_hour'] = final_df['monthly_spend'] / ((final_df['total_watch_minutes'].fillna(0) + 0.1) / 60)
        print("✔ 4. 파생 변수(시간당 비용) 계산 완료")

        # ---------------------------------------------------------
        # 결측치 처리 및 컬럼명 정리 (요청 사항 반영)
        # ---------------------------------------------------------
        final_df['devices_used'] = final_df['devices_used'].fillna(1).astype(int)
        final_df['completion_rate'] = final_df['completion_rate'].fillna(0)
        
        # 컬럼명 매핑 (1번 카테고리 요청 반영)
        mapping = {
            'subscription_plan': 'subscription_type',
            'monthly_spend': 'monthly_fee'
        }
        final_df = final_df.rename(columns=mapping)

        # ---------------------------------------------------------
        # 최종 10개 컬럼 순서 재배치
        # ---------------------------------------------------------
        cols = [
            # 1. 직접 추출
            'age', 'gender', 'country', 'subscription_type', 'primary_device', 'monthly_fee', 
            # 2. 계산/가공
            'account_age_months', 'devices_used', 
            # 3. 파생 변수
            'completion_rate', 'cost_per_hour'
        ]
        
        result = final_df[cols]

        print("\n" + "="*70)
        print(f"✔ 통합 완료: 총 {len(result)}명의 데이터가 10개의 컬럼으로 정제되었습니다.")
        print("="*70)
        print(result.head())
        
        return result

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    df = verify_refine_logic()