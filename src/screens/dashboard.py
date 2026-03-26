import streamlit as st
from src.components.metrics import render_metrics_row
from src.components.charts import render_trend_section

def render_dashboard():
    """
    메인 대시보드 화면을 렌더링합니다.
    _1/code.html 의 메인 컨텐츠 영역에 해당합니다.
    """
    
    # Page Header
    header_html = """
        <div class="page-header">
            <h2 class="page-title">
                📊 고객 모니터링 대시보드
            </h2>
            <p class="page-description">
                데이터 기반 고객 경험 최적화 및 이탈 예측 분석
            </p>
        </div>
    """
    st.html(header_html)
    
    # Section 1: KPI Metrics Row
    render_metrics_row()
    
    st.html('<div class="spacer-2_5"></div>')
    
    # Section 2: Main Trend Chart 
    render_trend_section()
