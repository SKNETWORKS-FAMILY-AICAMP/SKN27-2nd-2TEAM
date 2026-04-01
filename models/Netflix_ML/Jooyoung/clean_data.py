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

        # 2. 날짜 처리 (errors='coerce' 추가로 안전하게)
        users['subscription_start_date'] = pd.to_datetime(users['subscription_start_date'], errors='coerce')
        # 결측치가 생길 수 있으므로 dropna 또는 fillna 처리
        ref_date = users['subscription_start_date'].max()
        
        # 3. 사용 기기 수 계산 (컬럼 존재 확인 후 concat)
        log_list = []
        for df, name in zip([watch, search, recommend], ['watch', 'search', 'recommend']):
            if 'device_type' in df.columns:
                log_list.append(df[['user_id', 'device_type']])
            else:
                print(f"⚠ 경고: {name} 로그에 'device_type'이 없습니다.")

        if log_list:
            combined_logs = pd.concat(log_list).drop_duplicates()
            device_counts = combined_logs.groupby('user_id')['device_type'].nunique().reset_index()
            device_counts.columns = ['user_id', 'devices_used']
        else:
            # 로그에 기기 정보가 전혀 없을 경우 대비
            device_counts = pd.DataFrame(columns=['user_id', 'devices_used'])

        # 4. 컬럼명 매핑 및 정제
        mapping = {
            'age': 'age',
            'gender': 'gender',
            'country': 'country',
            'subscription_plan': 'subscription_type',
            'monthly_spend': 'monthly_fee',
            'primary_device': 'primary_device'
        }
        
                # 가져오고자 하는 전체 컬럼 리스트
        base_cols = ['user_id', 'age', 'gender', 'country', 'subscription_plan', 
                    'monthly_spend', 'primary_device', 'account_age_months']

        # 1) 실제로 users 데이터프레임에 존재하는 컬럼만 선별
        existing_cols = [c for c in base_cols if c in users.columns]

        # 2) 안전하게 추출 (KeyError 방지)
        refined = users[existing_cols].copy()

        # 3) 컬럼명 변경 (기존 mapping 사용)
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