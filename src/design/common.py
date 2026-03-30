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
}

def get_common_css():
    """
    앱 전역 CSS. 폰트·배경·메인 패딩·컬럼 간격·페이지 헤더(.page-header)·스페이서 등
    사이드바/지표/차트 모듈과 겹치지 않는 공통 레이어만 둡니다.
    """
    return textwrap.dedent(f"""
        /* --- 타이포: 본문 폰트 + 아이콘 폰트 로드 (대시보드·사이드바 공통) --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');

        /* --- 전역 타이포·배경: Streamlit 루트와 위젯 래퍼 기본 글꼴·색 --- */
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif !important;
            background-color: {COLORS["background"]};
            color: {COLORS["text_main"]};
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        /* --- 앱 셸: 메인 캔버스 배경 (사이드바 제외 영역) --- */
        .stApp {{
            background-color: {COLORS["background"]};
        }}

        /* --- 상단 헤더: 기본 흰 배경을 없애 전체 배경과 이어지게 (햄버거·테마 등 유지) --- */
        header[data-testid="stHeader"] {{
            background-color: transparent !important;
        }}
        
        /* --- 메인 콘텐츠 폭·여백: wide 레이아웃에서 좌우 패딩·최대 너비 (Stitch 레이아웃에 맞춤) --- */
        .main .block-container {{
            padding-top: 3rem !important; 
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            padding-bottom: 5rem !important;
            max-width: 1600px !important; /* Stitch 컨테이너 사이즈 */
        }}

        /* --- 컬럼: st.columns 간 시각적 간격 (카드 그리드 정렬) --- */
        [data-testid="column"] {{
            padding: 0 0.5rem !important;
        }}
        
        /* --- 마크다운 블록: 카드형 st.markdown이 가로 100%를 쓰도록 (줄바꿈·넘침 방지) --- */
        .element-container > .stMarkdown {{
            width: 100%;
        }}
        
        /* --- 페이지 타이틀 블록: Home / Analysis 상단 제목·설명 (markup.page_header_* 와 짝) --- */
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
        
        /* --- 세로 여백: 섹션 사이 빈 div (markup.spacer_std 등) --- */
        .spacer-2_5 {{
            height: 2.5rem;
        }}
    """)
