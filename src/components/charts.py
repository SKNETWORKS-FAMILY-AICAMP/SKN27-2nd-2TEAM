import streamlit as st
from src.design import markup
from src.design.common import COLORS
from src.utils.data_loader import load_ui_config, load_chart_data


def render_main_trend_chart():
    """
    데이터 로더를 통해 로드된 데이터로 트렌드 차트를 그립니다.
    """
    ui_config = load_ui_config()
    chart_config = ui_config["charts"]["trend_section"]

    st.html(
        markup.chart_trend_header(chart_config["icon"], chart_config["title"])
    )

    df = load_chart_data()
    st.area_chart(
        df,
        x="week",
        y="active_users",
        color=COLORS["primary"],
        height=320,
    )


def render_trend_section():
    """
    트렌드 차트를 포함하는 섹션 렌더링
    """
    with st.container(border=True):
        render_main_trend_chart()
