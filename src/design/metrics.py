import textwrap
from src.design.common import COLORS

def _css_metric_card_base() -> str:
    """metric-card 기본 박스/호버 인터랙션 스타일."""
    return f"""
        .metric-card {{
            background-color: {COLORS["surface"]};
            border-radius: 0.75rem;
            padding: 1.5rem;
            border: 1px solid {COLORS["border"]};
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s, box-shadow 0.2s;
            height: 100%;
        }}
        .metric-card:hover {{
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transform: translateY(-2px);
        }}
    """


def _css_icon_badges() -> str:
    """아이콘 배지 공통 + variant(primary/secondary/orange/tertiary)."""
    return """
        .icon-badge {
            padding: 0.5rem;
            border-radius: 0.5rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }
        .icon-badge.primary { background-color: #fef2f2; color: #b91c1c; }
        .icon-badge.secondary { background-color: #eff6ff; color: #1d4ed8; }
        .icon-badge.orange { background-color: #fff7ed; color: #c2410c; }
        .icon-badge.tertiary { background-color: #f0fdfa; color: #0f766e; }
    """


def _css_change_tags() -> str:
    """증감 태그(+/-)와 카드 헤더 정렬 스타일."""
    return f"""
        .change-tag {{
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
        }}
        .change-tag.positive {{ background-color: #f0fdf4; color: {COLORS["success"]}; }}
        .change-tag.negative {{ background-color: #fef2f2; color: {COLORS["danger"]}; }}
        .metric-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }}
    """


def _css_metric_typography() -> str:
    """KPI 카드 제목/값/이모지 타이포 스타일."""
    return f"""
        .metric-card-title {{
            font-size: 0.625rem;
            font-weight: 700;
            color: {COLORS["text_soft"]};
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin: 0 0 0.25rem 0;
        }}
        .metric-card-value {{
            font-size: 1.875rem;
            font-weight: 900;
            color: {COLORS["text_main"]};
            margin: 0;
            display: flex;
            align-items: baseline;
            gap: 0.25rem;
        }}
        .metric-card-emoji {{
            font-size: 0.875rem;
            font-weight: 400;
            color: #cbd5e1;
        }}
    """


def get_metrics_css():
    """`metric-card`·`icon-badge`·`change-tag` CSS."""
    return textwrap.dedent(
        "\n".join(
            [
                _css_metric_card_base(),
                _css_icon_badges(),
                _css_change_tags(),
                _css_metric_typography(),
            ]
        )
    )
