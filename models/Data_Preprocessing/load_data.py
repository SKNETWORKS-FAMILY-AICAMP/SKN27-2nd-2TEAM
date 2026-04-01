import random
import easydict
import pandas as pd
from utils import reset_seeds
from Netflix_ML.JAEKANG.something import NetflixFeatureBuilder

reset_seeds(42)

# ─────────────────────────────────────────
# 1. 경로 설정
# ─────────────────────────────────────────
def get_args(default_path: str = 'C:/dev/project/SKN27-2nd-2TEAM/models/data/') -> easydict.EasyDict:
    """경로 및 파일 설정을 담은 EasyDict 반환"""
    args = easydict.EasyDict()
    args.default_path = default_path

    # 넷플릭스 원본 데이터
    args.users_csv        = default_path + 'users.csv'
    args.watch_csv        = default_path + 'watch_history.csv'
    args.movies_csv       = default_path + 'movies.csv'
    args.rec_logs_csv     = default_path + 'recommendation_logs.csv'
    args.search_logs_csv  = default_path + 'search_logs.csv'
    args.reviews_csv      = default_path + 'reviews.csv'

    # 생성할 파일 경로
    args.train_csv               = default_path + 'Netflix_train.csv'
    args.test_csv                = default_path + 'Netflix_test.csv'
    args.submission_filename     = 'Netflix_submission.csv'
    args.default_submission_csv  = default_path + args.submission_filename
    args.save_results            = default_path + 'Netflix_results.json'

    # 분석용 설정
    args.random_state = 21
    args.results      = []

    return args


# ─────────────────────────────────────────
# 2. 데이터 로드
# ─────────────────────────────────────────
def load_data(args: easydict.EasyDict) -> dict:
    """CSV 파일들을 읽어 DataFrame dict로 반환"""
    data = {
        'user'       : pd.read_csv(args.users_csv).drop_duplicates(),
        'watch'      : pd.read_csv(args.watch_csv).drop_duplicates(),
        'movies'     : pd.read_csv(args.movies_csv).drop_duplicates(),
        'rec_logs'   : pd.read_csv(args.rec_logs_csv).drop_duplicates(),
        'search_logs': pd.read_csv(args.search_logs_csv).drop_duplicates(),
        'reviews'    : pd.read_csv(args.reviews_csv).drop_duplicates(),
    }

    data['user'] = refine_user_features(data['user'], data)
    data['user'] = build_features(data['user'], data)

    data['user'] = preprocess_target(data['user'])


    return data


# ─────────────────────────────────────────
# 3. Target 변환
# ─────────────────────────────────────────
def preprocess_target(users_df: pd.DataFrame) -> pd.DataFrame:
    """is_active → is_churned 변환 후 반환"""
    df = users_df.copy()

# 1. 변환 로직: is_active가 있으면 변환하고 원본 삭제
    if 'is_active' in df.columns:
        df['is_churned'] = 1 - df['is_active']
        df = df.drop(columns=['is_active'], errors='ignore')
    
    # 2. 만약 이미 is_churned가 있는 상태라면 아무것도 안 함 (중복 실행 방지)
    return df

# ─────────────────────────────────────────
# 4. 유저 기본 피처 정제  (verify_refine_logic 로직)
# ─────────────────────────────────────────
def refine_user_features(users_df: pd.DataFrame, data: dict) -> pd.DataFrame:
    df = users_df.copy()

    # 1. 계정 생성 개월수 계산
    df['subscription_start_date'] = pd.to_datetime(df['subscription_start_date'])
    ref_date = df['subscription_start_date'].max()
    df['account_age_months'] = (
        (ref_date.year  - df['subscription_start_date'].dt.year)  * 12
    + (ref_date.month - df['subscription_start_date'].dt.month)
    )

    # 2. 사용 기기 수 계산
    combined_logs = pd.concat([
        data['watch'][['user_id', 'device_type']],
        data['search_logs'][['user_id', 'device_type']],
        data['rec_logs'][['user_id', 'device_type']],
    ]).drop_duplicates()

    device_counts = (
        combined_logs
        .groupby('user_id')['device_type']
        .nunique()
        .reset_index()
        .rename(columns={'device_type': 'devices_used'})
    )

    # 3. 컬럼명 변경
    df = df.rename(columns={
        'subscription_plan': 'subscription_type',
        'monthly_spend'    : 'monthly_fee',
    })

    # 4. devices_used 병합 및 결측치 처리
    df = pd.merge(df, device_counts, on='user_id', how='left')
    df['devices_used'] = df['devices_used'].fillna(1).astype(int)

    return df


# ─────────────────────────────────────────
# 5. 파생 피처 빌딩  (NetflixFeatureBuilder 로직)
# ─────────────────────────────────────────
def build_features(users_df: pd.DataFrame, data: dict) -> pd.DataFrame:
    builder = NetflixFeatureBuilder(
        user = users_df,
        watch = data['watch'],
        reviews = data['reviews'],
        rec_logs = data['rec_logs'],
        search_logs = data['search_logs'],
        movies = data['movies'],
    )

    result = (
        builder
        .add_recommendation_click_rate()
        .add_content_interactions()
        .add_rating_given()
        .add_completion_rate()
        .add_watch_sessions_per_week()
        .add_avg_watch_time_minutes()
        .add_favorite_genre()
        .add_last_activity_date()
        .get_data()
    )
    return result

