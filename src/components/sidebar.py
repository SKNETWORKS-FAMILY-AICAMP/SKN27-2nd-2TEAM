import streamlit as st
import textwrap
from src.utils.data_loader import load_ui_config

def render_sidebar():
    """
    사이드바 메뉴와 하단 프로필을 렌더링합니다.
    Streamlit의 st.sidebar 컨텍스트 내에서 호출되어야 합니다.
    """
    ui_config = load_ui_config()
    sidebar_config = ui_config["sidebar"]

    # 헤더
    st.sidebar.html(
        f"""
        <div class="sidebar-header">
            <h1 class="sidebar-title">{sidebar_config['title']}</h1>
            <p class="sidebar-subtitle">{sidebar_config['subtitle']}</p>
        </div>
        """
    )

    # 세션 상태 초기화
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    # 내비게이션 메뉴
    menu_options = list(sidebar_config["menu"].keys())
    menu_labels = sidebar_config["menu"]
    
    # 원래 옵션 이름을 얻기 위해 역방향 매핑 생성
    display_options = [menu_labels[opt] for opt in menu_options]
    
    # 현재 인덱스를 찾아 초기 상태 설정 (없는 경우)
    current_idx = menu_options.index(st.session_state.current_page)
    initial_display = display_options[current_idx]

    # 세션 상태에 nav_radio가 없으면 초기화
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
