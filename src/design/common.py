import textwrap

# Colors
COLORS = {
    "primary": "#b81120",
    "secondary": "#005db6",
    "surface_low": "#f2f4f8",
    "surface_lowest": "#ffffff"
}

def get_common_css():
    """
    앱 전체에 공통적으로 적용되는 기본 CSS 스타일을 반환합니다.
    (폰트, 레이아웃 조정, Streamlit 기본 설정 오버라이드 등)
    """
    return textwrap.dedent("""
        /* Google Fonts & Material Symbols */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            background-color: #f2f4f8; /* surface-container-low */
            color: #191c1f; /* on-surface */
        }

        /* Streamlit Main Background */
        .stApp {
            background-color: #f2f4f8;
        }

        /* Make top header transparent instead of hiding it, so expand button is visible */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }
        
        /* Global Adjustments */
        .main .block-container {
            padding-top: 2rem !important; 
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            padding-bottom: 5rem !important;
            max-width: 100%;
        }

        /* Streamlit columns gap adjustment */
        [data-testid="column"] {
            padding: 0 !important;
        }
        
        /* Fix markdown container margin to prevent cards from overflowing or stacking incorrectly */
        .element-container > .stMarkdown {
            width: 100%;
        }
        
        /* Ensure containers stretch to fill height in flex columns */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            height: 100%;
        }
        div[data-testid="stVerticalBlock"] {
            height: 100%;
        }
        
        /* Page Header Common Styles */
        .page-header {
            margin-bottom: 2.5rem;
        }
        
        .page-title {
            font-size: 1.875rem;
            font-weight: 800;
            color: #191c1f;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            letter-spacing: -0.025em;
            margin: 0;
        }
        
        .page-description {
            margin-top: 0.5rem;
            color: #64748b;
            font-weight: 500;
            font-size: 1rem;
        }
        
        /* Spacer */
        .spacer-2_5 {
            height: 2.5rem;
        }
    """)