import streamlit as st
import pandas as st_pd
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
    
    # 캐싱된 차트 데이터 로드
    df = load_chart_data()
    
    # Streamlit line_chart 로 대체 (더 부드럽고 네이티브한 경험을 위해)
    # df의 'week' 컬럼을 인덱스로 설정하여 x축으로 사용
    chart_data = df.set_index('week')
    
    # Streamlit 네이티브 차트는 커스터마이징에 한계가 있으므로,
    # 시각적 유사도를 위해 간단한 커스텀 HTML/SVG 또는 Altair를 사용할 수 있지만
    # 여기서는 요구사항에 맞게 Streamlit area_chart/line_chart를 사용하되 색상을 primary로 맞춤
    st.line_chart(chart_data, color=COLORS["primary"], height=250)


def render_trend_section():
    """
    트렌드 차트를 포함하는 섹션 렌더링
    """
    with st.container():
        st.html('<div class="metric-card h-full">')
        render_main_trend_chart()
        st.html('</div>')
