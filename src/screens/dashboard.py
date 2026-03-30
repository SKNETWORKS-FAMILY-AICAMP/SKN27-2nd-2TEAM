"""
Home 라우트 화면: Netflix 스타일 대시보드 메인.

구성: 페이지 헤더 → KPI 행 → 트렌드 차트 → 하단 3모듈.
`main.py`에서 `current_page == "Home"` 일 때만 호출됩니다.
"""
import streamlit as st
from src.components.metrics import render_metrics_row
from src.components.charts import render_trend_section
from src.components.dashboard_modules import render_dashboard_modules
from src.design import markup
from src.utils.data_loader import load_ui_config


def render_dashboard():
    """
    메인 대시보드 화면을 렌더링합니다.
    _1/code.html 의 메인 컨텐츠 영역에 해당합니다.
    """
    ui_config = load_ui_config()
    header_config = ui_config["dashboard"]["header"]

    st.html(markup.page_header_simple(header_config["title"], header_config["description"]))

    render_metrics_row()

    st.html(markup.spacer_std())

    render_trend_section()

    render_dashboard_modules()
