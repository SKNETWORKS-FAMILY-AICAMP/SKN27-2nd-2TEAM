"""
앱에서 쓰는 JSON/CSV 파일 로드 및 Streamlit 캐시(`@st.cache_data`).

- 경로 상수는 `src.config.config` 참조
- UI 문자열: `ui_config.json`, 지표/차트/시뮬레이터/하단모듈: `data/sample/` 하위 파일
"""
import json
import pandas as pd
import streamlit as st
from src.config.config import (
    UI_CONFIG_PATH,
    METRICS_DATA_PATH,
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
    """지표 데이터 CSV 파일을 로드하여 리스트 형태로 반환합니다."""
    df = pd.read_csv(METRICS_DATA_PATH)
    # boolean 값 변환
    df['is_positive'] = df['is_positive'].astype(str).str.lower() == 'true'
    # NaN 처리
    df = df.fillna("")
    return df.to_dict('records')

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
