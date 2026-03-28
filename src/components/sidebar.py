import streamlit as st
from src.design import markup
from src.utils.data_loader import load_ui_config


def render_sidebar():
    """
    사이드바 메뉴와 하단 프로필을 렌더링합니다.
    Streamlit의 st.sidebar 컨텍스트 내에서 호출되어야 합니다.
    """
    ui_config = load_ui_config()
    sidebar_config = ui_config["sidebar"]

    st.sidebar.html(
        markup.sidebar_header(sidebar_config["title"], sidebar_config["subtitle"])
    )

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    menu_options = list(sidebar_config["menu"].keys())
    menu_labels = sidebar_config["menu"]

    display_options = [menu_labels[opt] for opt in menu_options]

    current_idx = menu_options.index(st.session_state.current_page)
    initial_display = display_options[current_idx]

    if "nav_radio" not in st.session_state:
        st.session_state.nav_radio = initial_display

    st.sidebar.radio(
        "Navigation",
        options=display_options,
        key="nav_radio",
        label_visibility="collapsed",
    )

    selected_display = st.session_state.nav_radio
    for key, val in menu_labels.items():
        if val == selected_display:
            st.session_state.current_page = key
            break

    st.sidebar.html(markup.sidebar_spacer())
