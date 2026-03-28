import textwrap

def get_charts_css():
    """
    차트 영역(charts) 컴포넌트에만 적용되는 CSS 스타일을 반환합니다.
    """
    return textwrap.dedent("""
        /* 차트 카드 컨테이너 */
        .chart-card {
            background-color: #ffffff; /* bg-white */
            border-radius: 0.75rem; /* rounded-xl */
            padding: 2rem; /* p-8 */
            border: 1px solid #f1f5f9; /* border-slate-100 */
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* shadow-sm */
        }
        
        /* 차트 섹션 헤더 */
        .chart-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem; /* mb-8 */
        }
        
        .chart-title-wrapper {
            display: flex;
            align-items: center;
            gap: 0.75rem; /* gap-3 */
        }
        
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
        
        .chart-icon-box .material-symbols-outlined {
            font-size: 0.875rem; /* text-sm */
        }
        
        .chart-title {
            font-size: 1.125rem; /* text-lg */
            font-weight: 700; /* font-bold */
            color: #0f172a; /* text-slate-900 */
            margin: 0;
        }
        
        /* 유틸리티 */
        .h-full {
            height: 100%;
        }
    """)
