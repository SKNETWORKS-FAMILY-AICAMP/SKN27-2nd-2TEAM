import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from utils import reset_seeds
from IPython.display import display

# ─────────────────────────────────────────
# 1. 인코딩 컬럼 분리
# ─────────────────────────────────────────
def get_encode_cols(train: pd.DataFrame) -> tuple:
    """범주형(object/category) 컬럼과 수치형 컬럼 분리."""
    enc_cols = train.select_dtypes(include=["object", "category"]).columns.tolist()
    normal_cols = [col for col in train.columns if col not in enc_cols]

    print(f'enc_cols    : {enc_cols}')
    print(f'normal_cols : {normal_cols}')

    return enc_cols, normal_cols


# ─────────────────────────────────────────
# 2. 범주형 인코딩
# ─────────────────────────────────────────
def encode_features(
    train: pd.DataFrame,
    test: pd.DataFrame,
    enc_cols: list,
    normal_cols: list,
    encoder_type: str = "hybrid",
    unique_threshold: int = 5,
) -> tuple:
    """encoder_type(onehot/label/hybrid)에 따라 인코딩을 수행한다."""

    reset_seeds(42)
    encoder_type = encoder_type.lower().strip()
    if encoder_type not in {"onehot", "label", "hybrid"}:
        raise ValueError(f"지원하지 않는 encoder_type: {encoder_type}")

    print(f'before: {train.shape} / {test.shape}')
    print(f'encoder_type: {encoder_type} (unique_threshold={unique_threshold})')

    # 범주형 컬럼이 없다면 수치형만 사용한다.
    if not enc_cols:
        print("categorical columns not found, skip encoding")
        enc_tr = train[normal_cols].reset_index(drop=True).copy()
        enc_te = test[normal_cols].reset_index(drop=True).copy()
        encoder_bundle = {
            "encoder_type": encoder_type,
            "low_card_cols": [],
            "high_card_cols": [],
            "feature_names": list(enc_tr.columns),
        }
        return enc_tr, enc_te, encoder_bundle

    tr_cat = train[enc_cols].astype(str)
    te_cat = test[enc_cols].astype(str)

    # train 기준 유니크 수로 low/high cardinality 컬럼을 분리한다.
    nunique_series = tr_cat.nunique(dropna=True)
    low_card_cols = [col for col in enc_cols if nunique_series[col] <= unique_threshold]
    high_card_cols = [col for col in enc_cols if nunique_series[col] > unique_threshold]

    if encoder_type == "onehot":
        low_card_cols = enc_cols[:]
        high_card_cols = []
    elif encoder_type == "label":
        low_card_cols = []
        high_card_cols = enc_cols[:]

    print(f"low_card_cols ({len(low_card_cols)}): {low_card_cols}")
    print(f"high_card_cols({len(high_card_cols)}): {high_card_cols}")

    ohe_encoder = None
    ord_encoder = None
    tr_blocks = [train[normal_cols].reset_index(drop=True)]
    te_blocks = [test[normal_cols].reset_index(drop=True)]

    if low_card_cols:
        # low-card는 onehot으로 안전하게 확장한다.
        ohe_encoder = OneHotEncoder(handle_unknown='ignore')
        tmp_tr_ohe = pd.DataFrame(
            ohe_encoder.fit_transform(tr_cat[low_card_cols]).toarray(),
            columns=ohe_encoder.get_feature_names_out(low_card_cols)
        )
        tmp_te_ohe = pd.DataFrame(
            ohe_encoder.transform(te_cat[low_card_cols]).toarray(),
            columns=ohe_encoder.get_feature_names_out(low_card_cols)
        )
        tr_blocks.append(tmp_tr_ohe.reset_index(drop=True))
        te_blocks.append(tmp_te_ohe.reset_index(drop=True))

    if high_card_cols:
        # high-card는 label(ordinal)로 차원 폭증을 막는다.
        ord_encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
        tmp_tr_ord = pd.DataFrame(
            ord_encoder.fit_transform(tr_cat[high_card_cols]),
            columns=[f"label__{col}" for col in high_card_cols]
        )
        tmp_te_ord = pd.DataFrame(
            ord_encoder.transform(te_cat[high_card_cols]),
            columns=[f"label__{col}" for col in high_card_cols]
        )
        tr_blocks.append(tmp_tr_ord.reset_index(drop=True))
        te_blocks.append(tmp_te_ord.reset_index(drop=True))

    # test에만 존재하는 신규 카테고리를 로깅한다.
    for col in enc_cols:
        unseen_values = sorted(set(te_cat[col]) - set(tr_cat[col]))
        if unseen_values:
            preview = unseen_values[:5]
            print(f"[warn] unseen categories in '{col}' (count={len(unseen_values)}): {preview}")

    enc_tr = pd.concat(tr_blocks, axis=1)
    enc_te = pd.concat(te_blocks, axis=1)

    print(f'after: {enc_tr.shape} / {enc_te.shape}')
    display(enc_tr.head())

    encoder_bundle = {
        "encoder_type": encoder_type,
        "onehot_encoder": ohe_encoder,
        "label_encoder": ord_encoder,
        "low_card_cols": low_card_cols,
        "high_card_cols": high_card_cols,
        "feature_names": list(enc_tr.columns),
    }
    return enc_tr, enc_te, encoder_bundle