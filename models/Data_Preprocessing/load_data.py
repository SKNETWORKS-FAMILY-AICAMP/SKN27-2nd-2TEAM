import random
import easydict
import pandas as pd
from utils import reset_seeds

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
        'user'       : pd.read_csv(args.users_csv),
        'watch'      : pd.read_csv(args.watch_csv),
        'movies'     : pd.read_csv(args.movies_csv),
        'rec_logs'   : pd.read_csv(args.rec_logs_csv),
        'search_logs': pd.read_csv(args.search_logs_csv),
        'reviews'    : pd.read_csv(args.reviews_csv),
    }
    return data


# ─────────────────────────────────────────
# 3. Target 변환
# ─────────────────────────────────────────
def preprocess_target(users_df: pd.DataFrame) -> pd.DataFrame:
    """is_active → is_churned 변환 후 반환"""
    df = users_df.copy()
    df['is_churned'] = 1 - df['is_active']
    df = df.drop(columns=['is_active'])
    return df



