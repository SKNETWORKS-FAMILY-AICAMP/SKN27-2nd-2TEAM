import json
import pandas as pd
import streamlit as st
from src.config.config import UI_CONFIG_PATH, METRICS_DATA_PATH, CHART_DATA_PATH

@st.cache_data
def load_ui_config():
    """UI 설정 JSON 파일을 로드합니다."""
    with open(UI_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_metrics_data():
    """지표 데이터 JSON 파일을 로드합니다."""
    with open(METRICS_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_chart_data():
    """차트 데이터 CSV 파일을 로드합니다."""
    return pd.read_csv(CHART_DATA_PATH)
