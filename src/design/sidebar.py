import textwrap
from src.design.common import COLORS

def _css_sidebar_shell() -> str:
    """사이드바 패널 배경 및 Streamlit 기본 네비 숨김."""
    return f"""
        [data-testid="stSidebar"] {{
            background-color: {COLORS["background"]} !important;
        }}
        [data-testid="stSidebarNav"] {{
            display: none !important;
        }}
    """


def _css_sidebar_nav() -> str:
    """라디오 기반 커스텀 내비게이션 스타일."""
    return f"""
        div.stRadio > div[role="radiogroup"] {{ gap: 0.25rem; }}
        div.stRadio > div[role="radiogroup"] > label {{
            padding: 0.5rem 1rem !important;
            border-radius: 0.375rem !important;
            transition: all 0.2s !important;
            background-color: transparent;
        }}
        div.stRadio > div[role="radiogroup"] > label:hover {{
            background-color: rgba(226, 232, 240, 0.5) !important;
        }}
        div.stRadio > div[role="radiogroup"] > label[data-checked="true"] {{
            background-color: rgba(226, 232, 240, 0.5) !important;
            border-left: 4px solid {COLORS["primary_dark"]} !important;
            border-radius: 0 0.375rem 0.375rem 0 !important;
        }}
        div.stRadio > div[role="radiogroup"] > label[data-checked="true"] p {{
            color: {COLORS["primary_dark"]} !important;
            font-weight: 700 !important;
        }}
        div.stRadio p {{
            font-size: 0.875rem !important;
            color: #475569 !important;
            font-weight: 500 !important;
            letter-spacing: -0.025em !important;
        }}
        div.stRadio > div[role="radiogroup"] span[data-baseweb="radio"] div:first-child {{
            display: none !important;
        }}
    """


def _css_sidebar_header() -> str:
    """사이드바 브랜딩 헤더와 하단 스페이서 스타일."""
    return f"""
        .sidebar-header {{ padding: 1rem 0 2.5rem 0; }}
        .sidebar-title {{
            font-size: 1.25rem;
            font-weight: 900;
            color: {COLORS["text_main"]};
            margin: 0;
        }}
        .sidebar-subtitle {{
            font-size: 0.75rem;
            color: {COLORS["text_muted"]};
            font-weight: 500;
            letter-spacing: -0.025em;
            margin: 0;
        }}
        .sidebar-spacer {{
            flex-grow: 1;
            height: 30vh;
        }}
    """


def get_sidebar_css():
    """사이드바 전용 CSS."""
    return textwrap.dedent(
        "\n".join(
            [
                _css_sidebar_shell(),
                _css_sidebar_nav(),
                _css_sidebar_header(),
            ]
        )
    )
