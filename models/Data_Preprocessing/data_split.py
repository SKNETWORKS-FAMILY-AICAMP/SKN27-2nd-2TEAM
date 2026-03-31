import pandas as pd
from sklearn.model_selection import train_test_split

def split_data(
    netflix_users: pd.DataFrame, test_size: float = 0.2, random_state: int = 42
) -> dict:
    """유저 단위 데이터셋을 8:2(stratify)로 나눠 반환."""
    # 타겟 컬럼 기준으로 X/y를 분리한다.
    X = netflix_users.drop(columns=["is_churned"])
    y = netflix_users["is_churned"]

    # 클래스 비율을 유지하기 위해 stratify=y를 고정한다.
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # 후속 전처리를 위해 train/test 복사본을 함께 반환한다.
    train = X_tr.copy()
    test = X_te.copy()

    print(f"X_tr: {X_tr.shape}, X_te: {X_te.shape}")
    print(f"y_tr: {y_tr.shape}, y_te: {y_te.shape}")
    print(f"train: {train.shape}, test: {test.shape}")

    return {
        "X_tr": X_tr,
        "X_te": X_te,
        "y_tr": y_tr,
        "y_te": y_te,
        "train": train,
        "test": test,
    }