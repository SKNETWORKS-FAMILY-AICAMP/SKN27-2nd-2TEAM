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
    KPI_INACTIVE_DAYS_THRESHOLD,
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
    # KPI 계산의 원천 데이터(사용자 단위 샘플).
    df = pd.read_csv(KPI_SOURCE_DATA_PATH)
    # 카드 제목/아이콘/포맷/증감 해석 규칙 정의.
    kpi_defs = _load_dashboard_kpi_defs()

    # 기준일(예: 12-25)과 비교 기준일(기준일 - 7일).
    target_date = _build_target_date(KPI_TARGET_MONTH_DAY)
    previous_date = target_date - timedelta(days=KPI_DELTA_DAYS)

    # 두 시점의 스냅샷을 같은 규칙으로 계산한 뒤 카드로 조립.
    current = _compute_snapshot_metrics(df, target_date)
    previous = _compute_snapshot_metrics(df, previous_date)
    return _build_dashboard_kpi_records(current, previous, kpi_defs)


def _load_dashboard_kpi_defs() -> list[dict]:
    """대시보드 KPI 카드 메타 설정을 ui_config에서 읽습니다."""
    ui_cfg = load_ui_config()
    return ui_cfg["dashboard"]["kpi_cards"]


def _build_dashboard_kpi_records(current: dict, previous: dict, kpi_defs: list[dict]) -> list[dict]:
    """현재/비교 스냅샷과 카드 정의를 결합해 렌더링용 레코드 리스트를 만듭니다."""
    records = []
    for card in kpi_defs:
        # delta_source: 이 카드가 참조할 스냅샷 키(예: churn_rate, active_users).
        metric_key = card["delta_source"]
        current_metric = _resolve_metric_value(current, metric_key, card["value_format"])
        previous_metric = _resolve_metric_value(previous, metric_key, card["value_format"])
        records.append(
            _build_metric_record(
                icon_name=card["icon_name"],
                icon_style_class=card["icon_style_class"],
                title=card["title"],
                value_text=_format_metric_value(current_metric, card),
                change_text=_format_metric_delta(current_metric, previous_metric, card),
                is_positive=_is_positive_delta(current_metric, previous_metric, card),
                emoji=card.get("emoji", ""),
            )
        )
    return records


def _resolve_metric_value(snapshot: dict, metric_key: str, value_format: str) -> float:
    """스냅샷 값에서 카드 표시용 원시값을 계산합니다."""
    metric_value = float(snapshot.get(metric_key, 0.0))
    # 활성 유저 비율 카드는 churn_rate를 100-값으로 변환해 사용.
    if value_format == "percent_from_churn":
        return _active_rate_from_churn(metric_value)
    return metric_value


def _format_metric_value(value: float, card_cfg: dict) -> str:
    """카드 설정에 맞게 숫자 포맷(count/percent/float)을 적용합니다."""
    value_format = card_cfg["value_format"]
    if value_format == "count":
        return _format_count(value)
    if value_format == "percent" or value_format == "percent_from_churn":
        return _format_percent(value)
    if value_format == "float":
        return _format_float_with_unit(value, card_cfg.get("value_unit", ""))
    return str(value)


def _format_metric_delta(current: float, previous: float, card_cfg: dict) -> str:
    """증감 포맷 규칙(percent_change / inverse_percent_change)을 적용합니다."""
    delta_format = card_cfg["delta_format"]
    delta = _format_delta_percent(current, previous)
    return _invert_delta_sign(delta) if delta_format == "inverse_percent_change" else delta


def _is_positive_delta(current: float, previous: float, card_cfg: dict) -> bool:
    """카드별 증감 의미(up/down)에 따라 positive 여부를 계산합니다."""
    direction = card_cfg.get("is_positive_when", "up")
    return current >= previous if direction == "up" else current < previous


def _build_target_date(month_day_text: str) -> date:
    """`MM-DD` 문자열을 현재 연도로 해석해 기준일을 생성합니다."""
    month, day = [int(token) for token in str(month_day_text).split("-", maxsplit=1)]
    return date(date.today().year, month, day)


def _compute_snapshot_metrics(df: pd.DataFrame, as_of_date: date) -> dict:
    """특정 기준일의 KPI 스냅샷(4종 원시 수치)을 계산합니다."""
    target_date = _build_target_date(KPI_TARGET_MONTH_DAY)
    # 기준일 대비 과거 시점 보정치(일). 과거일수록 허용 임계값을 완화.
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
    # 기준일 기준 비활성 임계치(기본 30일)에 시점 보정치를 더해 이탈 판정.
    inactivity_churned = days_since_clean > (KPI_INACTIVE_DAYS_THRESHOLD + day_shift)
    is_churned = (churned_yes | inactivity_churned.fillna(False)).fillna(False)

    # 활성 유저: 이탈이 아닌 사용자.
    active_mask = ~is_churned
    active_users = int(active_mask.sum())

    watch_time = pd.to_numeric(df.get("avg_watch_time_minutes"), errors="coerce")
    avg_watch_time = watch_time[active_mask].mean()

    valid_rows = int(is_churned.shape[0])
    # 이탈률(%): 이탈 사용자 비율.
    churn_rate = (float(is_churned.sum()) / valid_rows * 100.0) if valid_rows else 0.0

    # 평균 미접속 기간은 시점 보정치만큼 역산해 계산.
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
    """KPI 카드 렌더링 공통 스키마(dict)를 생성합니다."""
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
    """NaN/None 형태 값을 안전하게 0.0으로 치환합니다."""
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
