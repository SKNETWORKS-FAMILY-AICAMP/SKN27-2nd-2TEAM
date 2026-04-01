import pandas as pd
import os
from something import NetflixFeatureBuilder

# 1. 경로 설정
default_path = 'C:/dev/project/SKN27-2nd-2TEAM/models/data/'
users_csv = default_path + 'users.csv'
watch_csv = default_path + 'watch_history.csv'
movies_csv = default_path + 'movies.csv'
rec_logs_csv = default_path + 'recommendation_logs.csv'
search_logs_csv = default_path + 'search_logs.csv'
reviews_csv = default_path + 'reviews.csv'

# 2. 데이터 로드
print("데이터 로딩 중...")
user = pd.read_csv(users_csv)
watch = pd.read_csv(watch_csv)
movies = pd.read_csv(movies_csv)
rec_logs = pd.read_csv(rec_logs_csv)
search_logs = pd.read_csv(search_logs_csv)
reviews = pd.read_csv(reviews_csv)

# 3. Feature Builder 실행
print("특징 생성 중...")
builder = NetflixFeatureBuilder(
    user=user,
    watch=watch,
    reviews=reviews,
    rec_logs=rec_logs,
    search_logs=search_logs,
    movies=movies
)

builder.add_recommendation_click_rate()
builder.add_content_interactions()
builder.add_rating_given()
builder.add_completion_rate()
builder.add_watch_sessions_per_week()
builder.add_avg_watch_time_minutes()
builder.add_favorite_genre()
builder.add_last_activity_date()

new_user = builder.get_data()

# churned 컬럼 생성: is_active가 False면 1(이탈), True면 0(유지)
new_user['churned'] = (new_user['is_active'] == False).astype(int)


# 4. new_user CSV 저장 (JAEKANG 폴더에 저장)
save_folder = 'C:/dev/project/SKN27-2nd-2TEAM/models/Netflix_ML/JAEKANG/'
save_file = 'new_user_with_features.csv'
save_full_path = os.path.join(save_folder, save_file)



# 데이터프레임 저장 (전체 데이터)
new_user.to_csv(save_full_path, index=False, encoding='utf-8-sig')

print(f"✔ [완료] {save_file} 파일이 저장되었습니다.")
print(f"경로: {os.path.abspath(save_full_path)}")
