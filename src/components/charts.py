import streamlit as st
import pandas as st_pd
import numpy as np
from src.design.styles import COLORS

def render_main_trend_chart():
    """
    가짜 데이터를 생성하여 Streamlit 네이티브 차트 또는 matplotlib으로 트렌드 차트를 그립니다.
    """
    st.html(
        """
        <div class="chart-header">
            <div class="chart-title-wrapper">
                <div class="chart-icon-box">
                    <span class="material-symbols-outlined">show_chart</span>
                </div>
                <h3 class="chart-title">Active User Growth Trend</h3>
            </div>
        </div>
        """
    )
    
    # 가짜 데이터 생성
    x = np.arange(1, 5) # 4 weeks
    y = np.array([80, 60, 75, 40, 60, 20, 30])
    
    # Streamlit line_chart 로 대체 (더 부드럽고 네이티브한 경험을 위해)
    chart_data = st_pd.DataFrame(
        np.array([[80, 60, 75, 40, 60, 20, 30]]).T,
        columns=["Active Users"]
    )
    
    # Streamlit 네이티브 차트는 커스터마이징에 한계가 있으므로,
    # 시각적 유사도를 위해 간단한 커스텀 HTML/SVG 또는 Altair를 사용할 수 있지만
    # 여기서는 요구사항에 맞게 Streamlit area_chart를 사용하되 색상을 primary로 맞춤
    st.line_chart(chart_data, color=COLORS["primary"], height=250)


def render_trend_section():
    """
    트렌드 차트를 포함하는 섹션 렌더링
    """
    with st.container():
        st.html('<div class="metric-card h-full">')
        render_main_trend_chart()
        st.html('</div>')
