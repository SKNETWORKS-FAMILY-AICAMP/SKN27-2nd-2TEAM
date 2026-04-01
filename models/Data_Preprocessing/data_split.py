import pandas as pd
from sklearn.model_selection import train_test_split

def split_data(Netflix_users: pd.DataFrame, ori_test: pd.DataFrame,
            test_size: float = 0.2, random_state: int = 42) -> dict:
    """X/y 분리 및 train/test split 후 결과 반환"""

    # 1. X(피처)와 y(타겟) 분리
    X = Netflix_users.drop(columns=['is_churned'])
    y = Netflix_users['is_churned']

    # 2. train/test split
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y,
        test_size    = test_size,
        random_state = random_state,
        stratify     = y
    )

    # 3. 복사본 생성
    train = X_tr.copy()
    train['is_churned'] = y_tr

    test = X_te.copy()
    test['is_churned'] = y_te
    ori_te = X_te.copy()

    # 결과 확인
    print(f'X_tr: {X_tr.shape}, X_te: {X_te.shape}')
    print(f'y_tr: {y_tr.shape}, y_te: {y_te.shape}')
    print(f'train: {train.shape}, test: {test.shape}, ori_te: {ori_te.shape}')

    return {'X_tr': X_tr, 'X_te': X_te, 'y_tr': y_tr, 'y_te': y_te,
            'train': train, 'test': test, 'ori_te': ori_te}