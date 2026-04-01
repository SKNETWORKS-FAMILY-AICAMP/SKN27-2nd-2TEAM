"""
KPI/트렌드 계산 전용 순수 로직 모듈.

- 데이터 입출력(JSON/CSV)은 하지 않고, 전달받은 DataFrame/설정값만 처리합니다.
"""
from __future__ import annotations

from datetime import date

import pandas as pd

from src.config.config import INACTIVE_DAYS_THRESHOLD


def build_target_date(month_day_text: str) -> date:
    """`MM-DD` 문자열을 현재 연도로 해석해 기준일을 생성합니다."""
    month, day = [int(token) for token in str(month_day_text).split("-", maxsplit=1)]
    return date(date.today().year, month, day)


def build_dashboard_kpi_records(current: dict, previous: dict, kpi_defs: list[dict]) -> list[dict]:
    """현재/비교 스냅샷과 카드 정의를 결합해 렌더링용 레코드 리스트를 만듭니다."""
    records = []
    for card in kpi_defs:
        metric_key = card["delta_source"]
        current_metric = _resolve_metric_value(current, metric_key, card["value_format"])
        previous_metric = _resolve_metric_value(previous, metric_key, card["value_format"])
        records.append(
            {
                "icon_name": card["icon_name"],
                "icon_style_class": card["icon_style_class"],
                "title": card["title"],
                "value": _format_metric_value(current_metric, card),
                "change_text": _format_metric_delta(current_metric, previous_metric, card),
                "is_positive": bool(_is_positive_delta(current_metric, previous_metric, card)),
                "emoji": card.get("emoji", ""),
            }
        )
    return records


def compute_snapshot_metrics(df: pd.DataFrame, *, target_date: date, as_of_date: date) -> dict:
    """특정 기준일의 KPI 스냅샷(4종 원시 수치)을 계산합니다."""
    day_shift = max((target_date - as_of_date).days, 0)
    days_since_raw = pd.to_numeric(df.get("days_since_last_login"), errors="coerce")
    days_since_clean = days_since_raw.clip(lower=0)
    is_churned = _compute_churn_mask(df, days_since_clean, day_shift=day_shift)

    active_mask = ~is_churned
    active_users = int(active_mask.sum())

    watch_time = pd.to_numeric(df.get("avg_watch_time_minutes"), errors="coerce")
    avg_watch_time = watch_time[active_mask].mean()

    valid_rows = int(is_churned.shape[0])
    churn_rate = (float(is_churned.sum()) / valid_rows * 100.0) if valid_rows else 0.0

    as_of_days_since = (days_since_clean - day_shift).clip(lower=0)
    avg_days_since_login = as_of_days_since.mean()

    return {
        "active_users": float(active_users),
        "avg_watch_time": _nan_to_zero(avg_watch_time),
        "churn_rate": _nan_to_zero(churn_rate),
        "avg_days_since_login": _nan_to_zero(avg_days_since_login),
    }


def build_age_active_histogram_data(
    df: pd.DataFrame,
    *,
    target_date: date,
    previous_date: date,
    current_label: str,
    previous_label: str,
) -> pd.DataFrame:
    """기준일/비교일의 연령대별 활성 유저 수 비교 DataFrame을 생성합니다."""
    ages = pd.to_numeric(df.get("age"), errors="coerce")
    valid_age = ages.notna() & (ages >= 0) & (ages <= 120)
    filtered = df.loc[valid_age].copy()
    filtered["age"] = ages.loc[valid_age].astype(int)
    filtered["age_group"] = filtered["age"].map(_age_group_label)

    current_shift = max((target_date - target_date).days, 0)
    previous_shift = max((target_date - previous_date).days, 0)
    days_since = pd.to_numeric(filtered.get("days_since_last_login"), errors="coerce").clip(lower=0)
    current_active = ~_compute_churn_mask(filtered, days_since, day_shift=current_shift)
    previous_active = ~_compute_churn_mask(filtered, days_since, day_shift=previous_shift)

    current_counts = filtered.loc[current_active, "age_group"].value_counts()
    previous_counts = filtered.loc[previous_active, "age_group"].value_counts()
    all_groups = sorted(set(current_counts.index) | set(previous_counts.index), key=_age_group_sort_key)

    return pd.DataFrame(
        {
            previous_label: [int(previous_counts.get(group, 0)) for group in all_groups],
            current_label: [int(current_counts.get(group, 0)) for group in all_groups],
        },
        index=all_groups,
    )


def _resolve_metric_value(snapshot: dict, metric_key: str, value_format: str) -> float:
    metric_value = float(snapshot.get(metric_key, 0.0))
    if value_format == "percent_from_churn":
        return 100.0 - metric_value
    return metric_value


def _format_metric_value(value: float, card_cfg: dict) -> str:
    value_format = card_cfg["value_format"]
    if value_format == "count":
        return f"{int(round(value)):,}"
    if value_format == "percent" or value_format == "percent_from_churn":
        return f"{value:.1f}%"
    if value_format == "float":
        return f"{value:.1f} {card_cfg.get('value_unit', '')}"
    return str(value)


def _format_metric_delta(current: float, previous: float, card_cfg: dict) -> str:
    delta_format = card_cfg["delta_format"]
    delta = _format_delta_percent(current, previous)
    return _invert_delta_sign(delta) if delta_format == "inverse_percent_change" else delta


def _is_positive_delta(current: float, previous: float, card_cfg: dict) -> bool:
    direction = card_cfg.get("is_positive_when", "up")
    return current >= previous if direction == "up" else current < previous


def _format_delta_percent(current: float, previous: float) -> str:
    if previous == 0:
        delta = 0.0 if current == 0 else 100.0
    else:
        delta = ((current - previous) / abs(previous)) * 100.0
    sign = "+" if delta >= 0 else "-"
    return f"{sign}{abs(delta):.1f}%"


def _invert_delta_sign(delta_text: str) -> str:
    text = str(delta_text).strip()
    if text.startswith("+"):
        return "-" + text[1:]
    if text.startswith("-"):
        return "+" + text[1:]
    return text


def _compute_churn_mask(df: pd.DataFrame, days_since_clean: pd.Series, *, day_shift: int) -> pd.Series:
    churned_yes = (
        df.get("churned", pd.Series(dtype=str))
        .astype(str)
        .str.strip()
        .str.lower()
        == "yes"
    )
    inactivity_churned = days_since_clean > (INACTIVE_DAYS_THRESHOLD + day_shift)
    return (churned_yes | inactivity_churned.fillna(False)).fillna(False)


def _nan_to_zero(value) -> float:
    if pd.isna(value):
        return 0.0
    return float(value)


def _age_group_label(age_value: int) -> str:
    age = int(age_value)
    if age <= 19:
        return "10대 이하"
    if age >= 60:
        return "60대 이상"
    decade = (age // 10) * 10
    return f"{decade}대"


def _age_group_sort_key(label: str) -> int:
    order = {
        "10대 이하": 10,
        "20대": 20,
        "30대": 30,
        "40대": 40,
        "50대": 50,
        "60대 이상": 60,
    }
    return order.get(str(label), 10_000)
