import streamlit as st
import textwrap

def render_sidebar():
    """
    사이드바 메뉴와 하단 프로필을 렌더링합니다.
    Streamlit의 st.sidebar 컨텍스트 내에서 호출되어야 합니다.
    """
    # Header
    st.sidebar.html(
        """
        <div class="sidebar-header">
            <h1 class="sidebar-title">Analytics Pro</h1>
            <p class="sidebar-subtitle">Precision Curator</p>
        </div>
        """
    )

    # Session state 초기화
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    # Navigation menu
    menu_options = ["Home", "Customer Analysis", "Model"]
    # Add icons to the labels just for display
    menu_labels = {
        "Home": "🏠 Home",
        "Customer Analysis": "📉 고객 분석",
        "Model": "⚙️ 모델 정보"
    }
    
    # We create a reversed mapping to get the original option name
    display_options = [menu_labels[opt] for opt in menu_options]
    
    # Find current index to set the initial state if not present
    current_idx = menu_options.index(st.session_state.current_page)
    initial_display = display_options[current_idx]

    # Initialize nav_radio in session state if it doesn't exist
    if "nav_radio" not in st.session_state:
        st.session_state.nav_radio = initial_display

    # 라디오 버튼 위젯 (key를 통해 상태를 동기화)
    st.sidebar.radio(
        "Navigation",
        options=display_options,
        key="nav_radio",
        label_visibility="collapsed"
    )
    
    # 위젯에서 선택된 값을 current_page 에 동기화
    selected_display = st.session_state.nav_radio
    for key, val in menu_labels.items():
        if val == selected_display:
            st.session_state.current_page = key
            break
    
    st.sidebar.html('<div class="sidebar-spacer"></div>')
