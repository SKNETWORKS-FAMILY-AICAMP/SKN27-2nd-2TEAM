import textwrap

def get_sidebar_css():
    """
    왼쪽 사이드바 전용. 배경·커스텀 내비(st.sidebar.radio)·헤더 HTML(.sidebar-*)·
    Streamlit 기본 네비 숨김 등 `sidebar.py` + `markup.sidebar_*` 와 맞춘 스타일입니다.
    """
    return textwrap.dedent("""
        /* --- 사이드바 패널 배경 (메인 영역과 톤 구분) --- */
        [data-testid="stSidebar"] {
            background-color: #f8fafc !important; /* slate-100 */
        }
        /* --- Streamlit 기본 페이지 목록 숨김 (커스텀 라디오만 사용) --- */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* --- 내비게이션: 라디오를 메뉴 버튼처럼 보이게 (호버·선택 강조) --- */
        div.stRadio > div[role="radiogroup"] {
            gap: 0.25rem;
        }
        div.stRadio > div[role="radiogroup"] > label {
            padding: 0.5rem 1rem !important;
            border-radius: 0.375rem !important;
            transition: all 0.2s !important;
            background-color: transparent;
        }
        div.stRadio > div[role="radiogroup"] > label:hover {
            background-color: rgba(226, 232, 240, 0.5) !important;
        }
        div.stRadio > div[role="radiogroup"] > label[data-checked="true"] {
            background-color: rgba(226, 232, 240, 0.5) !important;
            border-left: 4px solid #b81120 !important;
            border-radius: 0 0.375rem 0.375rem 0 !important;
        }
        div.stRadio > div[role="radiogroup"] > label[data-checked="true"] p {
            color: #b81120 !important;
            font-weight: 700 !important;
        }
        div.stRadio p {
            font-size: 0.875rem !important;
            color: #475569 !important;
            font-weight: 500 !important;
            letter-spacing: -0.025em !important;
        }
        /* --- 라디오 원형 UI 숨김 (텍스트만 메뉴 스타일) --- */
        div.stRadio > div[role="radiogroup"] span[data-baseweb="radio"] div:first-child {
            display: none !important;
        }
        /* --- 사이드바 상단 타이틀 (markup.sidebar_header) --- */
        .sidebar-header {
            padding: 1rem 0 2.5rem 0;
        }
        
        .sidebar-title {
            font-size: 1.25rem;
            font-weight: 900;
            color: #0f172a;
            margin: 0;
        }
        
        .sidebar-subtitle {
            font-size: 0.75rem;
            color: #64748b;
            font-weight: 500;
            letter-spacing: -0.025em;
            margin: 0;
        }
        
        /* --- 하단 영역 밀어 올리기용 플렉스 여백 (markup.sidebar_spacer) --- */
        .sidebar-spacer {
            flex-grow: 1;
            height: 30vh;
        }
    """)
