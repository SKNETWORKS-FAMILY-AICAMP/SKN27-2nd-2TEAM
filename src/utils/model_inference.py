"""
세그먼트 슬라이싱 + 모델 추론 유틸.

- simulator_sample의 segment_name을 원본 사용자 데이터 필터 조건으로 매핑
- `model_netflix.pkl` 로드 후 `predict_proba` 평균(%) 및 사용자별 확률(%) 배열
- 폼 파라미터를 세그먼트 row 전체에 일괄 적용한 after 예측 계산
"""

from __future__ import annotations

from functools import lru_cache
import logging
import pickle
import warnings
from typing import Any

import numpy as np
import pandas as pd

from src.config.config import MODEL_PATH

logger = logging.getLogger(__name__)

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
    """
    사용자별 세그먼트 라벨을 `np.select`로 한 개만 부여합니다. 위에서 아래 순서로
    첫 번째로 참인 조건만 적용됩니다(앞 조건에 걸리면 뒤 조건은 평가되지 않음).

    1. subscription_plan ∈ {Premium, Premium+} → 프리미엄_가입군
    2. 1번이 거짓이고 primary_device == Mobile → 모바일_주사용군
    3. 1·2번이 거짓이고 household_size >= 3 → 다인가구군
    4. 1~3번이 거짓이고 start_year <= 2023 → 장기가입군
    5. 나머지 → 일반_안정군

    전처리 직후 `users_df`에 `subscription_plan`, `primary_device`, `household_size`, `start_year`가 있어야 합니다.
    """
    conds = [
        users_df["subscription_plan"].isin(["Premium", "Premium+"]),
        users_df["primary_device"] == "Mobile",
        users_df["household_size"] >= 3,
        users_df["start_year"] <= 2023,
    ]
    labels = [SEG_PREMIUM, SEG_MOBILE, SEG_LARGE_HOUSEHOLD, SEG_LONG_TERM]
    return pd.Series(np.select(conds, labels, default=SEG_GENERAL), index=users_df.index)


def slice_users_by_segment(users_df: pd.DataFrame, segment_name: str) -> pd.DataFrame:
    """
    `segment_name` 접두어가 가리키는 세그먼트 키에 맞는 행만 반환합니다.
    슬라이싱 규칙은 `_assign_segment_key`와 동일하며, `simulator_sample.csv` 괄호 설명과 맞춰 두어야 합니다.
    """
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


def _positive_churn_class_index(model: Any) -> int:
    """
    이진 분류에서 레이블 1(이탈, churned=1)에 해당하는 predict_proba 열 인덱스.

    학습 스크립트에서 churned = 1 - is_active 이므로 양성 클래스는 1입니다.
    `classes_`가 [0, 1]이면 보통 인덱스 1이 P(이탈)이나, 순서가 바뀐 모델에 대비합니다.
    """
    classes = getattr(model, "classes_", None)
    if classes is not None and len(classes) == 2:
        arr = np.asarray(classes)
        if np.any(arr == 1):
            return int(np.flatnonzero(arr == 1)[0])
    return 1


def _churn_probs_column_to_percent(raw_scores: np.ndarray) -> np.ndarray:
    """
    predict_proba에서 뽑은 이탈 확률 열(보통 [0,1])을 퍼센트 스케일로 변환합니다.

    트리/부스팅에서 리프가 순수하면 proba가 정확히 0.0 또는 1.0만 나오는 것이 수학적으로
    정상일 수 있습니다(연속값이 아닌 것처럼 보임). `predict()`로 바꾼 것이 아닙니다.
    """
    raw_scores = np.asarray(raw_scores, dtype=np.float64)
    raw_mean = float(np.mean(raw_scores))
    if raw_mean <= 1.0:
        out = raw_scores * 100.0
    else:
        out = raw_scores.copy()
    return np.clip(out, 0.0, 100.0)


def _predict_churn_prob_mean_and_per_user_pct(
    model: Any, df_features: pd.DataFrame
) -> tuple[float, np.ndarray, np.ndarray]:
    """(세그먼트 평균 %, 행별 %, 행별 원시 P(이탈) [0,1]) 반환."""
    if not hasattr(model, "predict_proba"):
        raise ValueError("모델이 predict_proba를 지원하지 않습니다.")
    probs = model.predict_proba(df_features)
    if probs.ndim != 2 or probs.shape[1] < 2:
        raise ValueError("predict_proba 결과 형식이 올바르지 않습니다.")
    idx = _positive_churn_class_index(model)
    raw = np.asarray(probs[:, idx], dtype=np.float64)
    pct = _churn_probs_column_to_percent(raw)
    mean_pct = round(float(np.mean(pct)), 1)
    return mean_pct, pct, raw


def _apply_policy_to_segment(
    segment_df: pd.DataFrame,
    *,
    subscription_plan: str,
    primary_device: str,
    household_size: float | None,
    monthly_spend_percent_of_baseline: float,
) -> pd.DataFrame:
    """인코딩 직전 컬럼만 갱신합니다. `subscription_plan`은 `_encode_features` 서수 인코딩 입력입니다."""
    updated = segment_df.copy()
    if subscription_plan != "dontcare":
        updated["subscription_plan"] = subscription_plan
    if primary_device != "dontcare":
        updated["primary_device"] = primary_device
    if household_size is not None:
        updated["household_size"] = float(household_size)

    factor = float(monthly_spend_percent_of_baseline) / 100.0
    if factor != 1.0 and "monthly_spend" in updated.columns:
        ms = pd.to_numeric(updated["monthly_spend"], errors="coerce").fillna(0.0).to_numpy(dtype=np.float64)
        updated["monthly_spend"] = np.clip(ms * factor, 0.0, np.inf)
        if "monthly_spend_log" in updated.columns:
            updated["monthly_spend_log"] = np.log1p(updated["monthly_spend"].to_numpy(dtype=np.float64))

    return updated


def _require_inference_input_columns(df: pd.DataFrame) -> None:
    """슬라이싱·인코딩에 필요한 컬럼이 있는지 검사합니다."""
    for col in ("subscription_plan", "primary_device", "household_size", "start_year"):
        if col not in df.columns:
            raise ValueError(f"추론용 데이터에 필수 컬럼 '{col}'이 없습니다. 전처리 파이프라인을 확인하세요.")


def _warn_policy_vs_model_features(model: Any, expected_columns: list[str] | None) -> None:
    """시뮬에서 바꾸는 피처가 모델 입력에 없으면 경고합니다."""
    if not expected_columns:
        return
    names = list(expected_columns)
    if "subscription_plan" not in names:
        warnings.warn(
            "모델 feature_names_in_에 'subscription_plan'이 없습니다. 요금제 시뮬 효과가 없을 수 있습니다.",
            stacklevel=3,
        )
    if not any(n.startswith("primary_device") for n in names):
        warnings.warn(
            "모델 feature_names_in_에 primary_device 원-핫 열이 없습니다. 기기 시뮬 효과가 없을 수 있습니다.",
            stacklevel=3,
        )
    if "household_size" not in names:
        logger.debug("모델 feature_names_in_에 household_size 없음 — 가구원 시뮬이 반영되지 않을 수 있음")


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


def _build_segment_results_wide_df(
    segment_df: pd.DataFrame,
    current_probs: np.ndarray,
    projected_probs: np.ndarray,
    *,
    current_raw: np.ndarray | None = None,
    projected_raw: np.ndarray | None = None,
) -> pd.DataFrame:
    """
    차트·보내기 공통: 인코딩 전 세그먼트 행 전체 + 예측 열만 덧붙인 wide 테이블.
    행 순서는 추론 배열과 동일합니다.
    """
    n = len(segment_df)
    if len(current_probs) != n or len(projected_probs) != n:
        raise ValueError("세그먼트 행 수와 이탈확률 배열 길이가 일치하지 않습니다.")
    out = segment_df.reset_index(drop=True).copy()
    out["current_pct"] = np.asarray(current_probs, dtype=np.float64)
    out["projected_pct"] = np.asarray(projected_probs, dtype=np.float64)
    if current_raw is not None:
        if len(current_raw) != n:
            raise ValueError("current_raw 길이가 세그먼트와 일치하지 않습니다.")
        out["proba_churn_raw_current"] = np.asarray(current_raw, dtype=np.float64)
    if projected_raw is not None:
        if len(projected_raw) != n:
            raise ValueError("projected_raw 길이가 세그먼트와 일치하지 않습니다.")
        out["proba_churn_raw_projected"] = np.asarray(projected_raw, dtype=np.float64)
    return out


def infer_segment_current_and_projected_prob(
    users_df: pd.DataFrame,
    *,
    selected_segment_name: str,
    submitted: bool,
    subscription_plan: str,
    primary_device: str,
    household_size: float | None,
    monthly_spend_percent_of_baseline: float = 100.0,
) -> tuple[float, float, int, np.ndarray, np.ndarray, pd.DataFrame]:
    """
    세그먼트 기준 Before/After 평균 이탈확률(%), 세그먼트 크기,
    사용자별 현재/시뮬레이션 이탈확률(%) 배열, 차트용 결합 DataFrame을 반환합니다.
    """
    _require_inference_input_columns(users_df)
    segment_df = slice_users_by_segment(users_df, selected_segment_name)
    if segment_df.empty:
        raise ValueError("선택한 세그먼트에 해당하는 원본 데이터가 없습니다.")

    model = _load_model()
    
    # 모델에 저장된 피처 이름 가져오기
    expected_columns = getattr(model, "feature_names_in_", None)
    _warn_policy_vs_model_features(model, list(expected_columns) if expected_columns is not None else None)
    
    # 예측에 사용하지 않는 타겟 및 중간 변수 제거 (원본 데이터에 존재할 경우)
    if 'churned' in segment_df.columns:
        segment_df = segment_df.drop(columns=['churned'])

    current_features = _encode_features(segment_df, expected_columns)
    current_prob, current_probs, current_raw = _predict_churn_prob_mean_and_per_user_pct(
        model, current_features
    )
    chart_df = _build_segment_results_wide_df(
        segment_df,
        current_probs,
        current_probs.copy(),
        current_raw=current_raw,
        projected_raw=current_raw.copy(),
    )

    if not submitted:
        return (
            current_prob,
            current_prob,
            len(segment_df),
            current_probs,
            current_probs.copy(),
            chart_df,
        )

    updated_df = _apply_policy_to_segment(
        segment_df,
        subscription_plan=subscription_plan,
        primary_device=primary_device,
        household_size=household_size,
        monthly_spend_percent_of_baseline=monthly_spend_percent_of_baseline,
    )

    projected_features = _encode_features(updated_df, expected_columns)
    projected_prob, projected_probs, projected_raw = _predict_churn_prob_mean_and_per_user_pct(
        model, projected_features
    )
    chart_df = _build_segment_results_wide_df(
        segment_df,
        current_probs,
        projected_probs,
        current_raw=current_raw,
        projected_raw=projected_raw,
    )

    return (
        current_prob,
        projected_prob,
        len(segment_df),
        current_probs,
        projected_probs,
        chart_df,
    )
