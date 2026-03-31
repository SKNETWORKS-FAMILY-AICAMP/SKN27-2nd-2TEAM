"""
대시보드(Home) 메인 영역의 트렌드 차트 블록.

- `ui_config.json`의 `charts.trend_section` 제목·아이콘
- `netflix_user_sample.csv` 기반 연령대별 활성 유저 수 비교 히스토그램 표시
"""
import streamlit as st
from src.design import markup
from src.utils.data_loader import load_ui_config, load_age_active_histogram_data


def render_main_trend_chart():
    """
    데이터 로더를 통해 로드된 데이터로 트렌드 차트를 그립니다.
    """
    # 차트 제목/아이콘/높이는 ui_config를 단일 소스로 사용합니다.
    ui_config = load_ui_config()
    chart_config = ui_config["charts"]["trend_section"]

    # 기준일/비교일 연령대별 활성 유저 수 비교 데이터를 읽어 히스토그램으로 표시합니다.
    df = load_age_active_histogram_data()
    labels = list(df.columns)
    resolved_title = chart_config["title"]
    if len(labels) >= 2:
        resolved_title = f"{resolved_title} ({labels[0]} vs {labels[1]})"
    st.html(markup.chart_trend_header(chart_config["icon"], resolved_title))
    if chart_config.get("caption"):
        st.caption(chart_config["caption"])
    st.bar_chart(df, height=int(chart_config["height"]))


def render_trend_section():
    """
    트렌드 차트를 포함하는 섹션 렌더링
    """
    with st.container(border=True):
        render_main_trend_chart()
