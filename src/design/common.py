import textwrap

# 앱 전역에서 쓰는 팔레트 (차트 색상·인라인 스타일·CSS 변수 치환에 사용)
COLORS = {
    "primary": "#e50914",  # 메인 강조, 차트 시리즈, 브랜드 포인트
    "primary_light": "#fef2f2",  # primary 아이콘 배경·밝은 강조면
    "primary_dark": "#b91c1c",  # primary보다 진한 텍스트/아이콘
    "secondary": "#005db6",  # 보조 강조(링크·보조 브랜드 톤 등)
    "background": "#f8fafc",  # 앱·메인 영역 바탕
    "surface": "#ffffff",  # 카드·패널 등 올라오는 면
    "text_main": "#0f172a",  # 본문·제목 기본 글자색
    "text_muted": "#64748b",  # 부가 설명·보조 텍스트
    "border": "#f1f5f9",  # 구분선·카드 테두리
    "success": "#16a34a",
    "danger": "#dc2626",
    "info_light": "#f1f5f9",
    "text_soft": "#94a3b8",
}

def _css_font_imports() -> str:
    """전역 폰트(텍스트/아이콘) import 블록."""
    return """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');
    """


def _css_shell_and_layout() -> str:
    """앱 루트 배경, block-container 패딩/폭, 컬럼 간격 등 레이아웃 기본값."""
    return f"""
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif !important;
            background-color: {COLORS["background"]};
            color: {COLORS["text_main"]};
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        .stApp {{ background-color: {COLORS["background"]}; }}
        header[data-testid="stHeader"] {{ background-color: transparent !important; }}
        .main .block-container {{
            padding-top: 3rem !important;
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            padding-bottom: 5rem !important;
            max-width: 1600px !important;
        }}
        [data-testid="column"] {{ padding: 0 0.5rem !important; }}
        .element-container > .stMarkdown {{ width: 100%; }}
    """


def _css_page_header_and_spacing() -> str:
    """페이지 헤더 타이포와 공통 스페이서 클래스."""
    return f"""
        .page-header {{ margin-bottom: 2.5rem; }}
        .page-title {{
            font-size: 1.875rem;
            line-height: 2.25rem;
            font-weight: 800;
            color: {COLORS["text_main"]};
            display: flex;
            align-items: center;
            gap: 0.75rem;
            letter-spacing: -0.025em;
            margin: 0;
        }}
        .page-description {{
            margin-top: 0.5rem;
            color: {COLORS["text_muted"]};
            font-weight: 500;
            font-size: 1rem;
        }}
        .spacer-2_5 {{ height: 2.5rem; }}
    """


def get_common_css():
    """
    앱 전역 CSS. 폰트·배경·메인 패딩·컬럼 간격·페이지 헤더(.page-header)·스페이서 등.
    """
    return textwrap.dedent(
        "\n".join(
            [
                _css_font_imports(),
                _css_shell_and_layout(),
                _css_page_header_and_spacing(),
            ]
        )
    )
