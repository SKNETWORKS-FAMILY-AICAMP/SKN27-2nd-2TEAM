import streamlit as st
from src.components.metrics import render_metrics_row
from src.components.charts import render_trend_section
from src.utils.data_loader import load_ui_config

def render_dashboard():
    """
    메인 대시보드 화면을 렌더링합니다.
    _1/code.html 의 메인 컨텐츠 영역에 해당합니다.
    """
    ui_config = load_ui_config()
    header_config = ui_config["dashboard"]["header"]
    
    # 페이지 헤더
    header_html = f"""
        <div class="page-header">
            <h2 class="page-title">
                {header_config['title']}
            </h2>
            <p class="page-description">
                {header_config['description']}
            </p>
        </div>
    """
    st.html(header_html)
    
    # 섹션 1: KPI 지표 행
    render_metrics_row()
    
    st.html('<div class="spacer-2_5"></div>')
    
    # 섹션 2: 메인 트렌드 차트 
    render_trend_section()
