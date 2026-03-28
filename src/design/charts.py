import textwrap

def get_charts_css():
    """
    차트 영역(charts) 컴포넌트에만 적용되는 CSS 스타일을 반환합니다.
    """
    return textwrap.dedent("""
        /* 차트 섹션 헤더 */
        .chart-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
        }
        
        .chart-title-wrapper {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .chart-icon-box {
            width: 2rem;
            height: 2rem;
            border-radius: 0.25rem;
            background-color: #ffdad7;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #b81120;
        }
        
        .chart-icon-box .material-symbols-outlined {
            font-size: 1rem;
        }
        
        .chart-title {
            font-size: 1.125rem;
            font-weight: 700;
            color: #191c1f;
            margin: 0;
        }
        
        /* 유틸리티 */
        .h-full {
            height: 100%;
        }
    """)
