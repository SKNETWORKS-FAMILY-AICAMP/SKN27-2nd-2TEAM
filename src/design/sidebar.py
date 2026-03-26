import textwrap

def get_sidebar_css():
    """
    사이드바 컴포넌트에만 적용되는 CSS 스타일을 반환합니다.
    """
    return textwrap.dedent("""
        /* Keep sidebar visible and expanded */
        [data-testid="stSidebar"] {
            background-color: #f8fafc !important; /* slate-100 */
        }
        /* Keep sidebar visible, only hide the nav links */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Streamlit radio button 커스터마이징 (Navigation) */
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
        /* 라디오 버튼 동그라미 숨기기 */
        div.stRadio > div[role="radiogroup"] span[data-baseweb="radio"] div:first-child {
            display: none !important;
        }
        /* Sidebar Header */
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
        
        /* Sidebar Spacer */
        .sidebar-spacer {
            flex-grow: 1;
            height: 30vh;
        }
    """)
