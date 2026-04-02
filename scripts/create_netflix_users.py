"""
서버 CSV를 병합해 학습/분석용 사용자 테이블을 만드는 배치 스크립트.

기존 `src/utils/create_netflix_users.py`에 있던 로직을 scripts 영역으로 이동했습니다.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.Data_Preprocessing.merge_data import merge_all_data


def build_table_paths(base_dir: str) -> dict:
    """load_data.py의 args 역할: 테이블별 CSV 경로를 dict로 반환."""
    return {
        "user": os.path.join(base_dir, "users.csv"),
        "watch": os.path.join(base_dir, "watch_history.csv"),
        "movies": os.path.join(base_dir, "movies.csv"),
        "rec_logs": os.path.join(base_dir, "recommendation_logs.csv"),
        "search_logs": os.path.join(base_dir, "search_logs.csv"),
        "reviews": os.path.join(base_dir, "reviews.csv"),
    }


def load_server_data(paths: dict) -> dict:
    """load_data.py의 load_data와 같은 형태로 서버 CSV를 읽어 반환."""
    data = {}
    for key, file_path in paths.items():
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"필수 파일이 없습니다: {file_path}")
        data[key] = pd.read_csv(file_path)
    return data


def preprocess_target(users_df: pd.DataFrame) -> pd.DataFrame:
    """load_data.py 의존 없이 타겟 컬럼을 생성한다."""
    df = users_df.copy()
    if "is_active" not in df.columns:
        raise KeyError("'users.csv'에 'is_active' 컬럼이 없습니다.")
    df["is_churned"] = 1 - df["is_active"]
    return df.drop(columns=["is_active"])


def main():
    server_dir = os.path.join(PROJECT_ROOT, "data", "server")
    merged_output = os.path.join(server_dir, "netflix_user_merged.csv")
    users_output = os.path.join(server_dir, "netflix_users_preprocessed.csv")

    table_paths = build_table_paths(server_dir)
    data = load_server_data(table_paths)

    # model_netflex.py와 동일하게 user_id 기준 테이블 병합
    netflix = merge_all_data(
        user=data["user"],
        watch=data["watch"],
        movies=data["movies"],
        rec_logs=data["rec_logs"],
        search_logs=data["search_logs"],
        reviews=data["reviews"],
    )
    netflix.to_csv(merged_output, index=False, encoding="utf-8-sig")
    print(f"병합 데이터 저장 완료: {merged_output} / shape={netflix.shape}")

    # # 이후 학습 파이프라인에서 바로 쓸 수 있도록 타겟 전처리도 함께 저장
    # users_for_train = preprocess_target(data["user"])
    # users_for_train.to_csv(users_output, index=False, encoding="utf-8-sig")
    # print(f"타겟 전처리 데이터 저장 완료: {users_output} / shape={users_for_train.shape}")


if __name__ == "__main__":
    main()
