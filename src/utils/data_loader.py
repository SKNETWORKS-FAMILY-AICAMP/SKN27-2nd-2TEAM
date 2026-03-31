"""
앱에서 쓰는 JSON/CSV 파일 로드 및 Streamlit 캐시(`@st.cache_data`).

- 경로 상수는 `src.config.config` 참조
- UI 문자열·하단 모듈: `src/config/` JSON, 지표/차트/시뮬레이터: `data/sample/` CSV
"""
import json
from datetime import date, timedelta
import pandas as pd
import streamlit as st
from src.config.config import (
    UI_CONFIG_PATH,
    KPI_SOURCE_DATA_PATH,
    KPI_TARGET_MONTH_DAY,
    KPI_DELTA_DAYS,
    CHART_DATA_PATH,
    SIMULATOR_DATA_PATH,
    DASHBOARD_MODULES_DATA_PATH,
)

@st.cache_data
def load_ui_config():
    """UI 설정 JSON 파일을 로드합니다."""
    with open(UI_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_metrics_data():
    """홈 KPI 4종(활성 사용자/평균 시청시간/이탈률/평균 미접속일)을 계산해 반환합니다."""
    df = pd.read_csv(KPI_SOURCE_DATA_PATH)

    target_date = _build_target_date(KPI_TARGET_MONTH_DAY)
    previous_date = target_date - timedelta(days=KPI_DELTA_DAYS)

    current = _compute_snapshot_metrics(df, target_date)
    previous = _compute_snapshot_metrics(df, previous_date)

    return [
        _build_metric_record(
            icon_name="group",
            icon_style_class="primary",
            title="전체 사용자 수",
            value_text=_format_count(current["active_users"]),
            change_text=_format_delta_percent(current["active_users"], previous["active_users"]),
            is_positive=current["active_users"] >= previous["active_users"],
            emoji="",
        ),
        _build_metric_record(
            icon_name="schedule",
            icon_style_class="secondary",
            title="평균 시청시간",
            value_text=_format_float_with_unit(current["avg_watch_time"], "분"),
            change_text=_format_delta_percent(current["avg_watch_time"], previous["avg_watch_time"]),
            is_positive=current["avg_watch_time"] >= previous["avg_watch_time"],
            emoji="",
        ),
        _build_metric_record(
            icon_name="how_to_reg",
            icon_style_class="tertiary",
            title="활성 유저 비율",
            value_text=_format_percent(_active_rate_from_churn(current["churn_rate"])),
            change_text=_invert_delta_sign(
                _format_delta_percent(current["churn_rate"], previous["churn_rate"])
            ),
            is_positive=_active_rate_from_churn(current["churn_rate"])
            >= _active_rate_from_churn(previous["churn_rate"]),
            emoji="",
        ),
        _build_metric_record(
            icon_name="event_busy",
            icon_style_class="orange",
            title="평균 미접속 기간",
            value_text=_format_float_with_unit(current["avg_days_since_login"], "일"),
            change_text=_format_delta_percent(
                current["avg_days_since_login"],
                previous["avg_days_since_login"],
            ),
            # 미접속 기간은 증가할수록 부정적이므로 색상 기준을 반대로 적용.
            is_positive=current["avg_days_since_login"] < previous["avg_days_since_login"],
            emoji="",
        ),
    ]


def _build_target_date(month_day_text: str) -> date:
    """`MM-DD` 문자열을 현재 연도로 해석해 기준일을 생성합니다."""
    month, day = [int(token) for token in str(month_day_text).split("-", maxsplit=1)]
    return date(date.today().year, month, day)


def _compute_snapshot_metrics(df: pd.DataFrame, as_of_date: date) -> dict:
    """특정 기준일의 KPI 스냅샷(4종 원시 수치)을 계산합니다."""
    target_date = _build_target_date(KPI_TARGET_MONTH_DAY)
    day_shift = max((target_date - as_of_date).days, 0)

    churned_series = (
        df.get("churned", pd.Series(dtype=str))
        .astype(str)
        .str.strip()
        .str.lower()
    )
    churned_yes = churned_series == "yes"

    days_since_raw = pd.to_numeric(df.get("days_since_last_login"), errors="coerce")
    days_since_clean = days_since_raw.clip(lower=0)
    inactivity_churned = days_since_clean > (30 + day_shift)
    is_churned = (churned_yes | inactivity_churned.fillna(False)).fillna(False)

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


def _format_count(value: float) -> str:
    return f"{int(round(value)):,}"


def _format_float_with_unit(value: float, unit: str) -> str:
    return f"{value:.1f} {unit}"


def _format_percent(value: float) -> str:
    return f"{value:.1f}%"


def _format_delta_percent(current: float, previous: float) -> str:
    """이전값 대비 상대 증감률을 `+1.2%` 형식으로 반환합니다."""
    if previous == 0:
        delta = 0.0 if current == 0 else 100.0
    else:
        delta = ((current - previous) / abs(previous)) * 100.0
    sign = "+" if delta >= 0 else "-"
    return f"{sign}{abs(delta):.1f}%"


def _active_rate_from_churn(churn_rate: float) -> float:
    """이탈률(%)을 활성 유저 비율(%)로 변환합니다."""
    return 100.0 - churn_rate


def _invert_delta_sign(delta_text: str) -> str:
    """`+x%` <-> `-x%` 부호를 반전합니다."""
    text = str(delta_text).strip()
    if text.startswith("+"):
        return "-" + text[1:]
    if text.startswith("-"):
        return "+" + text[1:]
    return text


def _build_metric_record(
    icon_name: str,
    icon_style_class: str,
    title: str,
    value_text: str,
    change_text: str,
    is_positive: bool,
    emoji: str,
) -> dict:
    return {
        "icon_name": icon_name,
        "icon_style_class": icon_style_class,
        "title": title,
        "value": value_text,
        "change_text": change_text,
        "is_positive": bool(is_positive),
        "emoji": emoji,
    }


def _nan_to_zero(value) -> float:
    if pd.isna(value):
        return 0.0
    return float(value)

@st.cache_data
def load_chart_data():
    """차트 데이터 CSV 파일을 로드합니다."""
    return pd.read_csv(CHART_DATA_PATH)

@st.cache_data
def load_simulator_data():
    """시뮬레이터 샘플 데이터 CSV 파일을 로드합니다."""
    return pd.read_csv(SIMULATOR_DATA_PATH)


@st.cache_data
def load_dashboard_modules_data():
    """대시보드 하단 3모듈용 JSON 데이터를 로드합니다."""
    with open(DASHBOARD_MODULES_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
