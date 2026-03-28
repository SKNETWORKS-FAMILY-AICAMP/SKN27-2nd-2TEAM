import streamlit as st
from src.design.styles import inject_custom_css
from src.components.sidebar import render_sidebar
from src.screens.dashboard import render_dashboard
from src.screens.analysis import render_analysis

def main():
    # 1. Streamlit 페이지 기본 설정
    st.set_page_config(
        page_title="Customer Insights - Analytics Pro",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 2. 커스텀 CSS 주입 (디자인 시스템 적용)
    inject_custom_css()
    
    # 3. 사이드바 렌더링 (여기서 st.session_state.current_page 가 설정됨)
    render_sidebar()
    
    # 4. 메인 화면 라우팅
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
        
    current_page = st.session_state.current_page
    
    if current_page == "Home":
        render_dashboard()
    elif current_page == "Analysis":
        render_analysis()

if __name__ == "__main__":
    main()
