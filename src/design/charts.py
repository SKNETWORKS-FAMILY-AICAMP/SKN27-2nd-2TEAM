import textwrap
from src.design.common import COLORS

def _css_chart_card() -> str:
    """chart-card 컨테이너 및 높이 유틸 클래스."""
    return f"""
        .chart-card {{
            background-color: {COLORS["surface"]};
            border-radius: 0.75rem;
            padding: 2rem;
            border: 1px solid {COLORS["border"]};
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        }}
        .h-full {{ height: 100%; }}
    """


def _css_chart_header() -> str:
    """차트 제목 행 레이아웃(chart-header/title-wrapper)."""
    return """
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
    """


def _css_chart_icon_and_title() -> str:
    """차트 제목 아이콘 박스와 제목 타이포 스타일."""
    return f"""
        .chart-icon-box {{
            width: 2rem;
            height: 2rem;
            border-radius: 0.25rem;
            background-color: {COLORS["primary_light"]};
            display: flex;
            align-items: center;
            justify-content: center;
            color: {COLORS["primary_dark"]};
        }}
        .chart-icon-box .material-symbols-outlined {{ font-size: 0.875rem; }}
        .chart-title {{
            font-size: 1.125rem;
            font-weight: 700;
            color: {COLORS["text_main"]};
            margin: 0;
        }}
    """


def get_charts_css():
    """`chart-card`/`chart-header` 관련 CSS."""
    return textwrap.dedent(
        "\n".join(
            [
                _css_chart_card(),
                _css_chart_header(),
                _css_chart_icon_and_title(),
            ]
        )
    )
