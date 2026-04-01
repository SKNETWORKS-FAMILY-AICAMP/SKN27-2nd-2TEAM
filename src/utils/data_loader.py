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
    load_ui_config_dict,
    UI_CONFIG_PATH,
    KPI_SOURCE_DATA_PATH,
    SNAPSHOT_TARGET_MONTH_DAY,
    SNAPSHOT_DELTA_DAYS,
    SIMULATOR_DATA_PATH,
    DASHBOARD_MODULES_DATA_PATH,
)
from src.utils.metrics_service import (
    build_age_active_histogram_data,
    build_dashboard_kpi_records,
    build_target_date,
    compute_snapshot_metrics,
)

@st.cache_data
def load_ui_config():
    """UI 설정 JSON 파일을 로드합니다."""
    return load_ui_config_dict()

@st.cache_data
def load_metrics_data():
    """홈 KPI 4종(활성 사용자/평균 시청시간/이탈률/평균 미접속일)을 계산해 반환합니다."""
    # KPI 계산의 원천 데이터(사용자 단위 샘플).
    df = pd.read_csv(KPI_SOURCE_DATA_PATH)
    # 카드 제목/아이콘/포맷/증감 해석 규칙 정의.
    kpi_defs = _load_dashboard_kpi_defs()

    # 기준일(예: 12-25)과 비교 기준일(기준일 - 7일).
    target_date = build_target_date(SNAPSHOT_TARGET_MONTH_DAY)
    previous_date = target_date - timedelta(days=SNAPSHOT_DELTA_DAYS)

    # 두 시점의 스냅샷을 같은 규칙으로 계산한 뒤 카드로 조립.
    current = compute_snapshot_metrics(df, target_date=target_date, as_of_date=target_date)
    previous = compute_snapshot_metrics(df, target_date=target_date, as_of_date=previous_date)
    return build_dashboard_kpi_records(current, previous, kpi_defs)


def _load_dashboard_kpi_defs() -> list[dict]:
    """대시보드 KPI 카드 메타 설정을 ui_config에서 읽습니다."""
    ui_cfg = load_ui_config()
    return ui_cfg["dashboard"]["kpi_cards"]


@st.cache_data
def load_age_active_histogram_data() -> pd.DataFrame:
    """기준일/비교일의 연령대별 활성 유저 수 비교 DataFrame을 생성합니다."""
    ui_config = load_ui_config()
    trend_cfg = ui_config["charts"]["trend_section"]
    target_date = build_target_date(SNAPSHOT_TARGET_MONTH_DAY)
    previous_date = target_date - timedelta(days=SNAPSHOT_DELTA_DAYS)
    current_label = trend_cfg.get("current_label") or target_date.strftime("%m/%d")
    previous_label = trend_cfg.get("previous_label") or previous_date.strftime("%m/%d")

    df = pd.read_csv(KPI_SOURCE_DATA_PATH)
    return build_age_active_histogram_data(
        df,
        target_date=target_date,
        previous_date=previous_date,
        current_label=current_label,
        previous_label=previous_label,
    )

@st.cache_data
def load_simulator_data():
    """시뮬레이터 샘플 데이터 CSV 파일을 로드합니다."""
    return pd.read_csv(SIMULATOR_DATA_PATH)


@st.cache_data
def load_dashboard_modules_data():
    """대시보드 하단 3모듈용 JSON 데이터를 로드합니다."""
    with open(DASHBOARD_MODULES_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
