import streamlit as st
from src.design.common import get_common_css, COLORS
from src.design.sidebar import get_sidebar_css
from src.design.metrics import get_metrics_css
from src.design.charts import get_charts_css
from src.utils.data_loader import load_ui_config


def apply_streamlit_page_config():
    """브라우저 탭 제목·아이콘·wide 레이아웃 등 앱 셸 설정 (`ui_config.app`)."""
    cfg = load_ui_config().get("app") or {}
    st.set_page_config(
        page_title=cfg.get("page_title", "Streamlit"),
        page_icon=cfg.get("page_icon"),
        layout=cfg.get("layout", "centered"),
        initial_sidebar_state=cfg.get("initial_sidebar_state", "auto"),
    )


def inject_custom_css():
    """
    Precision Curator 흐름으로 공통·사이드바·지표·차트 CSS를 한 번에 `<style>`로 주입합니다.
    순서는 캐스케이딩 우선순위를 고려해 공통 → 영역별입니다.
    """
    # 레이아웃·폰트·페이지 헤더·컬럼 등 전역
    common_css = get_common_css()

    # 왼쪽 내비·사이드바 HTML 블록
    sidebar_css = get_sidebar_css()
    # metric-card / icon-badge / KPI 타이포
    metrics_css = get_metrics_css()
    # chart-header / chart-card
    charts_css = get_charts_css()

    combined_css = f"""
    <style>
    {common_css}

    /* 사이드바 전용 */
    {sidebar_css}

    /* KPI·카드·배지 */
    {metrics_css}

    /* 차트 헤더·chart-card */
    {charts_css}
    </style>
    """
    
    st.markdown(combined_css, unsafe_allow_html=True)
