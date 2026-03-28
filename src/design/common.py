import textwrap

# 색상 (Stitch Tailwind Config + Tailwind 기본 색상 참조)
COLORS = {
    "primary": "#e50914", # Netflix Red 느낌 (Stitch에서는 b81120 / FF4B4B 혼용)
    "primary_light": "#fef2f2", # bg-red-50
    "primary_dark": "#b91c1c", # text-red-700
    "secondary": "#005db6",
    "background": "#f8fafc", # bg-slate-50
    "surface": "#ffffff", # bg-white
    "text_main": "#0f172a", # text-slate-900
    "text_muted": "#64748b", # text-slate-500
    "border": "#f1f5f9" # border-slate-100
}

def get_common_css():
    """
    앱 전체에 공통적으로 적용되는 기본 CSS 스타일을 반환합니다.
    (폰트, 레이아웃 조정, Streamlit 기본 설정 오버라이드 등)
    """
    return textwrap.dedent(f"""
        /* 구글 폰트 및 머티리얼 심볼 */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif !important;
            background-color: {COLORS["background"]};
            color: {COLORS["text_main"]};
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        /* Streamlit 메인 배경 */
        .stApp {{
            background-color: {COLORS["background"]};
        }}

        /* 확장 버튼이 보이도록 상단 헤더를 숨기지 않고 투명하게 만듦 */
        header[data-testid="stHeader"] {{
            background-color: transparent !important;
        }}
        
        /* 전역 조정 */
        .main .block-container {{
            padding-top: 3rem !important; 
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            padding-bottom: 5rem !important;
            max-width: 1600px !important; /* Stitch 컨테이너 사이즈 */
        }}

        /* Streamlit 컬럼 간격 조정 */
        [data-testid="column"] {{
            padding: 0 0.5rem !important;
        }}
        
        /* 카드가 넘치거나 잘못 쌓이는 것을 방지하기 위해 마크다운 컨테이너 여백 수정 */
        .element-container > .stMarkdown {{
            width: 100%;
        }}
        
        /* 페이지 헤더 공통 스타일 (Stitch 디자인 기반) */
        .page-header {{
            margin-bottom: 2.5rem;
        }}
        
        .page-title {{
            font-size: 1.875rem; /* text-3xl */
            line-height: 2.25rem;
            font-weight: 800; /* font-extrabold */
            color: {COLORS["text_main"]};
            display: flex;
            align-items: center;
            gap: 0.75rem;
            letter-spacing: -0.025em; /* tracking-tight */
            margin: 0;
        }}
        
        .page-description {{
            margin-top: 0.5rem;
            color: {COLORS["text_muted"]};
            font-weight: 500; /* font-medium */
            font-size: 1rem;
        }}
        
        /* 여백 */
        .spacer-2_5 {{
            height: 2.5rem;
        }}
    """)
