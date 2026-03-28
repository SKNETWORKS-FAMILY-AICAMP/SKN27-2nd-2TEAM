import streamlit as st
from src.design.common import get_common_css, COLORS
from src.design.sidebar import get_sidebar_css
from src.design.metrics import get_metrics_css
from src.design.charts import get_charts_css

def inject_custom_css():
    """
    DESIGN.md 의 'Precision Curator' 테마를 반영한 커스텀 CSS
    각 컴포넌트 및 페이지별 세분화된 CSS 모듈들을 합쳐서 주입합니다.
    """
    
    # 1. 공통 CSS
    common_css = get_common_css()
    
    # 2. 컴포넌트별 CSS
    sidebar_css = get_sidebar_css()
    metrics_css = get_metrics_css()
    charts_css = get_charts_css()
    
    # 통합 CSS 생성
    combined_css = f"""
    <style>
    {common_css}
    
    /* --- 사이드바 스타일 --- */
    {sidebar_css}
    
    /* --- 지표 스타일 --- */
    {metrics_css}
    
    /* --- 차트 스타일 --- */
    {charts_css}
    </style>
    """
    
    st.markdown(combined_css, unsafe_allow_html=True)
