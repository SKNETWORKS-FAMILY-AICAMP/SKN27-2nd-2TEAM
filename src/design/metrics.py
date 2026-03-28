import textwrap

def get_metrics_css():
    """
    KPI 카드(metrics) 컴포넌트에만 적용되는 CSS 스타일을 반환합니다.
    """
    return textwrap.dedent("""
        /* 지표 카드 - Stitch 대시보드 기준 */
        .metric-card {
            background-color: #ffffff; /* bg-white */
            border-radius: 0.75rem; /* rounded-xl */
            padding: 1.5rem; /* p-6 */
            border: 1px solid #f1f5f9; /* border-slate-100 */
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* shadow-sm */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s, box-shadow 0.2s;
            height: 100%;
        }
        
        .metric-card:hover {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transform: translateY(-2px);
        }

        /* 아이콘 배지 (Stitch 테마 컬러) */
        .icon-badge {
            padding: 0.5rem; /* p-2 */
            border-radius: 0.5rem; /* rounded-lg */
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }

        .icon-badge.primary { background-color: #fef2f2; color: #b91c1c; } /* bg-red-50 text-red-700 */
        .icon-badge.secondary { background-color: #eff6ff; color: #1d4ed8; } /* bg-blue-50 text-blue-700 */
        .icon-badge.orange { background-color: #fff7ed; color: #c2410c; } /* bg-orange-50 text-orange-700 */
        .icon-badge.tertiary { background-color: #f0fdfa; color: #0f766e; } /* bg-teal-50 text-teal-700 */

        /* 증감 태그 */
        .change-tag {
            font-size: 0.75rem; /* text-xs */
            font-weight: 700; /* font-bold */
            padding: 0.25rem 0.5rem; /* px-2 py-1 */
            border-radius: 0.25rem; /* rounded */
        }
        .change-tag.positive { background-color: #f0fdf4; color: #16a34a; } /* bg-green-50 text-green-600 */
        .change-tag.negative { background-color: #fef2f2; color: #dc2626; } /* bg-red-50 text-red-600 */
        
        /* 지표 카드 내부 요소들 */
        .metric-card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem; /* mb-4 */
        }
        
        .metric-card-title {
            font-size: 0.625rem; /* text-[10px] */
            font-weight: 700; /* font-bold */
            color: #94a3b8; /* text-slate-400 */
            text-transform: uppercase;
            letter-spacing: 0.1em; /* tracking-widest */
            margin: 0 0 0.25rem 0; /* mb-1 */
        }
        
        .metric-card-value {
            font-size: 1.875rem; /* text-3xl */
            font-weight: 900; /* font-black */
            color: #0f172a; /* text-slate-900 */
            margin: 0;
            display: flex;
            align-items: baseline;
            gap: 0.25rem;
        }
        
        .metric-card-emoji {
            font-size: 0.875rem; /* text-sm */
            font-weight: 400; /* font-normal */
            color: #cbd5e1; /* text-slate-300 */
        }
    """)
