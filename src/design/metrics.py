import textwrap

def get_metrics_css():
    """
    KPI 카드(metrics) 컴포넌트에만 적용되는 CSS 스타일을 반환합니다.
    """
    return textwrap.dedent("""
        /* 지표 카드 - 1단계 */
        .metric-card {
            background-color: #ffffff; /* surface-container-lowest */
            border-radius: 0.75rem; /* rounded-xl */
            padding: 1.5rem; /* p-6 */
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* shadow-sm */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .metric-card:hover {
            /* 앰비언트 그림자 */
            box-shadow: 0 12px 40px rgba(25, 28, 31, 0.06);
            transform: translateY(-2px);
        }

        /* 아이콘 배지 */
        .icon-badge {
            padding: 0.5rem;
            border-radius: 0.5rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }

        .icon-badge.primary { background-color: #ffdad7; color: #b81120; }
        .icon-badge.secondary { background-color: #d6e3ff; color: #005db6; }
        .icon-badge.orange { background-color: #ffedd5; color: #c2410c; }
        .icon-badge.tertiary { background-color: #7ff7df; color: #00685a; }

        /* 증감 태그 */
        .change-tag {
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
        }
        .change-tag.positive { background-color: #f0fdf4; color: #16a34a; }
        .change-tag.negative { background-color: #fef2f2; color: #dc2626; }
        
        /* 지표 카드 내부 요소들 */
        .metric-card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        
        .metric-card-title {
            font-size: 0.75rem;
            font-weight: 700;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin: 0 0 0.25rem 0;
        }
        
        .metric-card-value {
            font-size: 1.875rem;
            font-weight: 900;
            color: #191c1f;
            margin: 0;
        }
        
        .metric-card-emoji {
            font-size: 0.875rem;
            font-weight: 400;
            color: #94a3b8;
        }
    """)
