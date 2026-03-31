"""
대시보드(Home) 메인 영역의 트렌드 차트 블록.

- `ui_config.json`의 `charts.trend_section` 제목·아이콘
- `chart_data.csv` 시계열을 `st.area_chart`로 표시
"""
import streamlit as st
from src.design import markup
from src.design.common import COLORS
from src.utils.data_loader import load_ui_config, load_chart_data


def render_main_trend_chart():
    """
    데이터 로더를 통해 로드된 데이터로 트렌드 차트를 그립니다.
    """
    # 차트 제목/아이콘/높이는 ui_config를 단일 소스로 사용합니다.
    ui_config = load_ui_config()
    chart_config = ui_config["charts"]["trend_section"]

    st.html(
        markup.chart_trend_header(chart_config["icon"], chart_config["title"])
    )

    # chart_data.csv에서 주차별 active_users 시계열을 읽어 바로 렌더링합니다.
    df = load_chart_data()
    st.line_chart(
        df,
        x="week",
        y="active_users",
        color=COLORS["primary"],
        height=int(chart_config["height"]),
    )


def render_trend_section():
    """
    트렌드 차트를 포함하는 섹션 렌더링
    """
    with st.container(border=True):
        render_main_trend_chart()
