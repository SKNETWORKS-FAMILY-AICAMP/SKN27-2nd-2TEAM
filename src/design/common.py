import textwrap

# 색상
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
        /* 구글 폰트 및 머티리얼 심볼 */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            background-color: #f2f4f8; /* surface-container-low */
            color: #191c1f; /* on-surface */
        }

        /* Streamlit 메인 배경 */
        .stApp {
            background-color: #f2f4f8;
        }

        /* 확장 버튼이 보이도록 상단 헤더를 숨기지 않고 투명하게 만듦 */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }
        
        /* 전역 조정 */
        .main .block-container {
            padding-top: 2rem !important; 
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            padding-bottom: 5rem !important;
            max-width: 100%;
        }

        /* Streamlit 컬럼 간격 조정 */
        [data-testid="column"] {
            padding: 0 !important;
        }
        
        /* 카드가 넘치거나 잘못 쌓이는 것을 방지하기 위해 마크다운 컨테이너 여백 수정 */
        .element-container > .stMarkdown {
            width: 100%;
        }
        
        /* 플렉스 컬럼에서 컨테이너가 높이를 채우도록 확장 */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            height: 100%;
        }
        div[data-testid="stVerticalBlock"] {
            height: 100%;
        }
        
        /* 페이지 헤더 공통 스타일 */
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
        
        /* 여백 */
        .spacer-2_5 {
            height: 2.5rem;
        }
    """)