"""
세그먼트 슬라이싱 + 모델 추론 유틸.

- simulator_sample의 segment_name을 원본 사용자 데이터 필터 조건으로 매핑
- `model_netflix.pkl` 로드 후 `predict_proba` 평균(%) 및 사용자별 확률(%) 배열
- 폼 파라미터를 세그먼트 row 전체에 일괄 적용한 after 예측 계산
"""

from __future__ import annotations

from functools import lru_cache
import pickle
from typing import Any

import numpy as np
import pandas as pd

from src.config.config import MODEL_PATH


SEG_PREMIUM = "프리미엄_가입군"
SEG_MOBILE = "모바일_주사용군"
SEG_LARGE_HOUSEHOLD = "다인가구군"
SEG_LONG_TERM = "장기가입군"
SEG_GENERAL = "일반_안정군"


def _segment_key_from_label(segment_name: str) -> str:
    if segment_name.startswith(SEG_PREMIUM):
        return SEG_PREMIUM
    if segment_name.startswith(SEG_MOBILE):
        return SEG_MOBILE
    if segment_name.startswith(SEG_LARGE_HOUSEHOLD):
        return SEG_LARGE_HOUSEHOLD
    if segment_name.startswith(SEG_LONG_TERM):
        return SEG_LONG_TERM
    return SEG_GENERAL


def _assign_segment_key(users_df: pd.DataFrame) -> pd.Series:
    conds = [
        users_df["subscription_plan"].isin(["Premium", "Premium+"]),
        users_df["primary_device"] == "Mobile",
        users_df["household_size"] >= 3,
        users_df["start_year"] <= 2023,
    ]
    labels = [SEG_PREMIUM, SEG_MOBILE, SEG_LARGE_HOUSEHOLD, SEG_LONG_TERM]
    return pd.Series(np.select(conds, labels, default=SEG_GENERAL), index=users_df.index)


def slice_users_by_segment(users_df: pd.DataFrame, segment_name: str) -> pd.DataFrame:
    """segment_name에 해당하는 원본 row 슬라이스를 반환합니다."""
    target_key = _segment_key_from_label(segment_name)
    segment_keys = _assign_segment_key(users_df)
    return users_df[segment_keys == target_key].copy()


@lru_cache(maxsize=1)
def _load_model() -> Any:
    """모델 파일을 한 번만 로드합니다."""
    model_path = str(MODEL_PATH)
    try:
        import joblib  # type: ignore

        return joblib.load(model_path)
    except Exception:
        with open(model_path, "rb") as f:
            return pickle.load(f)


def _churn_probs_column_to_percent(raw_scores: np.ndarray) -> np.ndarray:
    """predict_proba 이탈 클래스 열을 KPI와 동일 스케일의 퍼센트 배열로 변환합니다."""
    raw_scores = np.asarray(raw_scores, dtype=np.float64)
    raw_mean = float(np.mean(raw_scores))
    if raw_mean <= 1.0:
        out = raw_scores * 100.0
    else:
        out = raw_scores.copy()
    return np.clip(out, 0.0, 100.0)


def _predict_churn_prob_mean_and_per_user_pct(
    model: Any, df_features: pd.DataFrame
) -> tuple[float, np.ndarray]:
    if not hasattr(model, "predict_proba"):
        raise ValueError("모델이 predict_proba를 지원하지 않습니다.")
    probs = model.predict_proba(df_features)
    if probs.ndim != 2 or probs.shape[1] < 2:
        raise ValueError("predict_proba 결과 형식이 올바르지 않습니다.")
    pct = _churn_probs_column_to_percent(probs[:, 1])
    mean_pct = round(float(np.mean(pct)), 1)
    return mean_pct, pct


def _apply_policy_to_segment(
    segment_df: pd.DataFrame,
    *,
    subscription_type: str,
    primary_device: str,
    household_size: float | None,
) -> pd.DataFrame:
    updated = segment_df.copy()
    if subscription_type != "dontcare":
        updated["subscription_type"] = subscription_type
        # 월별 지출은 요금제에 따라 달라지므로, 기존에 학습된 방식과 동일하게 
        # subscription_plan의 전체 평균으로 대치하거나, 여기서는 단순화하여 로그값을 유지할 수 있으나
        # 엄밀함을 위해 폼에서는 제외했으므로 원본 유지합니다.
    if primary_device != "dontcare":
        updated["primary_device"] = primary_device
    if household_size is not None:
        updated["household_size"] = float(household_size)
    return updated


def _encode_features(df: pd.DataFrame, expected_columns: list[str]) -> pd.DataFrame:
    """데이터프레임을 인코딩하고 모델의 기대 컬럼에 맞춥니다."""
    df_enc = df.copy()
    
    # 1. subscription_plan Ordinal Encoding
    plan_mapping = {'Basic': 0, 'Standard': 1, 'Premium': 2, 'Premium+': 3}
    if 'subscription_plan' in df_enc.columns:
        df_enc['subscription_plan'] = df_enc['subscription_plan'].map(plan_mapping).fillna(0)
    
    # 2. Categorical One-Hot Encoding
    cat_cols = ['gender', 'country', 'state_province', 'primary_device']
    present_cat_cols = [c for c in cat_cols if c in df_enc.columns]
    if present_cat_cols:
        df_enc = pd.get_dummies(df_enc, columns=present_cat_cols, drop_first=False)
    
    # 3. Align with expected columns
    if expected_columns is not None:
        # Add missing columns
        for col in expected_columns:
            if col not in df_enc.columns:
                df_enc[col] = False if col.startswith(tuple(cat_cols)) else 0
        # Select and order columns
        df_enc = df_enc[expected_columns]
        
    return df_enc


def infer_segment_current_and_projected_prob(
    users_df: pd.DataFrame,
    *,
    selected_segment_name: str,
    submitted: bool,
    subscription_type: str,
    primary_device: str,
    household_size: float | None,
) -> tuple[float, float, int, np.ndarray, np.ndarray]:
    """
    세그먼트 기준 Before/After 평균 이탈확률(%), 세그먼트 크기,
    사용자별 현재/시뮬레이션 이탈확률(%) 배열을 반환합니다.
    """
    segment_df = slice_users_by_segment(users_df, selected_segment_name)
    if segment_df.empty:
        raise ValueError("선택한 세그먼트에 해당하는 원본 데이터가 없습니다.")

    model = _load_model()
    
    # 모델에 저장된 피처 이름 가져오기
    expected_columns = getattr(model, "feature_names_in_", None)
    
    # 예측에 사용하지 않는 타겟 및 중간 변수 제거 (원본 데이터에 존재할 경우)
    if 'churned' in segment_df.columns:
        segment_df = segment_df.drop(columns=['churned'])

    current_features = _encode_features(segment_df, expected_columns)
    current_prob, current_probs = _predict_churn_prob_mean_and_per_user_pct(
        model, current_features
    )

    if not submitted:
        return current_prob, current_prob, len(segment_df), current_probs, current_probs.copy()

    updated_df = _apply_policy_to_segment(
        segment_df,
        subscription_type=subscription_type,
        primary_device=primary_device,
        household_size=household_size,
    )

    projected_features = _encode_features(updated_df, expected_columns)
    projected_prob, projected_probs = _predict_churn_prob_mean_and_per_user_pct(
        model, projected_features
    )

    return current_prob, projected_prob, len(segment_df), current_probs, projected_probs
