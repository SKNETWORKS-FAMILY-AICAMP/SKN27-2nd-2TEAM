import textwrap

def get_charts_css():
    """
    트렌드 차트 헤더(`chart-header`·`chart-icon-box`)와 분석 화면 AI 코멘트 등
    `chart-card` 클래스를 쓰는 HTML(`markup.chart_trend_header`·`analysis_ai_comment_card`)용.
    """
    return textwrap.dedent("""
        /* --- 카드형 래퍼: 흰 패널·테두리 (st.container(border)와 별도로 쓰는 커스텀 카드) --- */
        .chart-card {
            background-color: #ffffff; /* bg-white */
            border-radius: 0.75rem; /* rounded-xl */
            padding: 2rem; /* p-8 */
            border: 1px solid #f1f5f9; /* border-slate-100 */
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* shadow-sm */
        }
        
        /* --- 트렌드 차트 상단: 제목 줄 전체 (markup.chart_trend_header) --- */
        .chart-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem; /* mb-8 */
        }
        
        /* --- 아이콘 박스 + 제목 가로 정렬 --- */
        .chart-title-wrapper {
            display: flex;
            align-items: center;
            gap: 0.75rem; /* gap-3 */
        }
        
        /* --- 머티리얼 아이콘 네모 배경 (primary 톤) --- */
        .chart-icon-box {
            width: 2rem; /* w-8 */
            height: 2rem; /* h-8 */
            border-radius: 0.25rem; /* rounded */
            background-color: #fef2f2; /* bg-red-50 */
            display: flex;
            align-items: center;
            justify-content: center;
            color: #b91c1c; /* text-red-700 */
        }
        
        /* --- 아이콘 크기만 살짝 축소 --- */
        .chart-icon-box .material-symbols-outlined {
            font-size: 0.875rem; /* text-sm */
        }
        
        /* --- 차트 블록 제목 텍스트 --- */
        .chart-title {
            font-size: 1.125rem; /* text-lg */
            font-weight: 700; /* font-bold */
            color: #0f172a; /* text-slate-900 */
            margin: 0;
        }
        
        /* --- 카드 높이 맞춤: 컬럼 안에서 metric-card 등과 동일 높이 --- */
        .h-full {
            height: 100%;
        }
    """)
