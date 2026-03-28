import streamlit as st
from src.design.styles import COLORS
from src.utils.data_loader import load_ui_config, load_chart_data

def render_main_trend_chart():
    """
    데이터 로더를 통해 로드된 데이터로 트렌드 차트를 그립니다.
    """
    ui_config = load_ui_config()
    chart_config = ui_config["charts"]["trend_section"]
    
    st.html(
        f"""
        <div class="chart-header">
            <div class="chart-title-wrapper">
                <div class="chart-icon-box">
                    <span class="material-symbols-outlined">{chart_config['icon']}</span>
                </div>
                <h3 class="chart-title">{chart_config['title']}</h3>
            </div>
        </div>
        """
    )
    
    df = load_chart_data()
    # x/y를 명시해 단일 시리즈만 그리면, 다중 열일 때 나오는 시리즈 선택 UI가 생기지 않습니다.
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
