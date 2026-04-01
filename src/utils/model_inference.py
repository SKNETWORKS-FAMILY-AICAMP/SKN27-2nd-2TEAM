"""
세그먼트 슬라이싱 + 모델 추론 유틸.

- simulator_sample의 segment_name을 원본 사용자 데이터 필터 조건으로 매핑
- `model_Netflex.pkl` 로드 후 `predict_proba` 평균값(%) 계산
- 폼 파라미터를 세그먼트 row 전체에 일괄 적용한 after 예측 계산
"""

from __future__ import annotations

from functools import lru_cache
import pickle
from typing import Any

import numpy as np
import pandas as pd

from src.config.config import MODEL_PATH


SEG_NEW = "신규_온보딩군"
SEG_LOYAL = "충성_헤비시청군"
SEG_DORMANT = "휴면_위험군"
SEG_MOBILE = "모바일_라이트시청군"
SEG_PREMIUM = "프리미엄_헤비시청군"
SEG_GENERAL = "일반_안정군"


def _segment_key_from_label(segment_name: str) -> str:
    if segment_name.startswith(SEG_NEW):
        return SEG_NEW
    if segment_name.startswith(SEG_LOYAL):
        return SEG_LOYAL
    if segment_name.startswith(SEG_DORMANT):
        return SEG_DORMANT
    if segment_name.startswith(SEG_MOBILE):
        return SEG_MOBILE
    if segment_name.startswith(SEG_PREMIUM):
        return SEG_PREMIUM
    return SEG_GENERAL


def _assign_segment_key(users_df: pd.DataFrame) -> pd.Series:
    conds = [
        users_df["account_age_months"] <= 6,
        (users_df["account_age_months"] >= 36) & (users_df["avg_watch_time_minutes"] >= 200),
        (users_df["days_since_last_login"] >= 45) | (users_df["completion_rate"] <= 45),
        (users_df["primary_device"] == "Mobile") & (users_df["avg_watch_time_minutes"] < 120),
        (users_df["subscription_type"] == "Premium") & (users_df["avg_watch_time_minutes"] >= 180),
    ]
    labels = [SEG_NEW, SEG_LOYAL, SEG_DORMANT, SEG_MOBILE, SEG_PREMIUM]
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


def _to_probability_percent(raw_scores: np.ndarray) -> float:
    raw_mean = float(np.mean(raw_scores))
    if raw_mean <= 1.0:
        return round(raw_mean * 100.0, 1)
    return round(raw_mean, 1)


def _predict_churn_probability_pct(model: Any, df_features: pd.DataFrame) -> float:
    if not hasattr(model, "predict_proba"):
        raise ValueError("모델이 predict_proba를 지원하지 않습니다.")
    probs = model.predict_proba(df_features)
    if probs.ndim != 2 or probs.shape[1] < 2:
        raise ValueError("predict_proba 결과 형식이 올바르지 않습니다.")
    return _to_probability_percent(probs[:, 1])


def _apply_policy_to_segment(
    segment_df: pd.DataFrame,
    *,
    subscription_type: str,
    monthly_revenue: float,
    viewing_hours: float,
    support_calls: int,
) -> pd.DataFrame:
    updated = segment_df.copy()
    if subscription_type != "dontcare":
        updated["subscription_type"] = subscription_type
    if "monthly_fee" in updated.columns:
        updated["monthly_fee"] = float(monthly_revenue)
    if "avg_watch_time_minutes" in updated.columns:
        updated["avg_watch_time_minutes"] = float(viewing_hours) * 6.0
    if "days_since_last_login" in updated.columns:
        updated["days_since_last_login"] = int(np.clip(support_calls * 10, 0, 365))
    return updated


def infer_segment_current_and_projected_prob(
    users_df: pd.DataFrame,
    *,
    selected_segment_name: str,
    submitted: bool,
    subscription_type: str,
    monthly_revenue: float,
    viewing_hours: float,
    support_calls: int,
) -> tuple[float, float, int]:
    """
    세그먼트 기준 Before/After 평균 이탈확률(%)과 세그먼트 크기를 반환합니다.
    """
    # 데이터 슬라이싱 
    segment_df = slice_users_by_segment(users_df, selected_segment_name)
    if segment_df.empty:
        raise ValueError("선택한 세그먼트에 해당하는 원본 데이터가 없습니다.")

    # 데이터 슬라이스 한 시점에서 테이블 인코딩 적용 
    

    # 모델 로드 
    model = _load_model()

    # 변경 전 데이터로 모델 추론 
    current_prob = _predict_churn_probability_pct(model, segment_df)

    if not submitted:
        return current_prob, current_prob, len(segment_df)

    updated_df = _apply_policy_to_segment(
        segment_df,
        subscription_type=subscription_type,
        monthly_revenue=monthly_revenue,
        viewing_hours=viewing_hours,
        support_calls=support_calls,
    )
    projected_prob = _predict_churn_probability_pct(model, updated_df)
    return current_prob, projected_prob, len(segment_df)
