import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from utils import reset_seeds
from IPython.display import display

# ─────────────────────────────────────────
# 1. 인코딩 컬럼 분리
# ─────────────────────────────────────────
def get_encode_cols(train: pd.DataFrame) -> tuple:
    """범주형 컬럼과 수치형 컬럼 분리하여 반환"""

    enc_cols    = ['gender', 'subscription_plan', 'subscription_start_date', 'primary_device']
    normal_cols = list(set(train.columns) - set(enc_cols))

    print(f'enc_cols    : {enc_cols}')
    print(f'normal_cols : {normal_cols}')

    return enc_cols, normal_cols


# ─────────────────────────────────────────
# 2. OneHotEncoding
# ─────────────────────────────────────────
def encode_features(train: pd.DataFrame, test: pd.DataFrame,
                    enc_cols: list, normal_cols: list) -> tuple:
    """OneHotEncoding 수행 후 enc_tr, enc_te, encoder 반환"""

    reset_seeds(42)

    print(f'before: {train.shape} / {test.shape}')

    enc = OneHotEncoder()

    # train 인코딩 (fit + transform)
    tmp_tr = pd.DataFrame(
        enc.fit_transform(train[enc_cols]).toarray(),
        columns=enc.get_feature_names_out()
    )
    enc_tr = pd.concat(
        [train[normal_cols].reset_index(drop=True), tmp_tr.reset_index(drop=True)],
        axis=1
    )

    # test 인코딩 (transform only)
    tmp_te = pd.DataFrame(
        enc.transform(test[enc_cols]).toarray(),
        columns=enc.get_feature_names_out()
    )
    enc_te = pd.concat(
        [test[normal_cols].reset_index(drop=True), tmp_te.reset_index(drop=True)],
        axis=1
    )

    print(f'after: {enc_tr.shape} / {enc_te.shape}')
    display(enc_tr.head())

    return enc_tr, enc_te, enc