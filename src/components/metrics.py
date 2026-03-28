import streamlit as st
from src.design import markup
from src.utils.data_loader import load_metrics_data


def render_metric_card(icon_name, icon_style_class, title, value, change_text, is_positive=True, emoji=""):
    """
    KPI 지표 카드 컴포넌트 렌더링

    매개변수:
        icon_name (str): 머티리얼 심볼 아이콘 이름
        icon_style_class (str): 아이콘 배경용 CSS 클래스 (primary, secondary, orange, tertiary)
        title (str): 카드 제목
        value (str): 주요 지표 값
        change_text (str): 증감률 텍스트 (예: "+12.5%")
        is_positive (bool): 긍정적 변화일 경우 True, 부정적일 경우 False
        emoji (str): 값 뒤에 추가되는 선택적 이모지
    """
    st.html(
        markup.metric_card_html(
            icon_name,
            icon_style_class,
            title,
            value,
            change_text,
            is_positive=is_positive,
            emoji=emoji,
        )
    )


def render_metrics_row():
    """
    상단 4개의 KPI 지표 카드를 나란히 렌더링합니다.
    """
    metrics_data = load_metrics_data()
    cols = st.columns(4)

    for i, metric in enumerate(metrics_data[:4]):
        with cols[i]:
            render_metric_card(
                icon_name=metric["icon_name"],
                icon_style_class=metric["icon_style_class"],
                title=metric["title"],
                value=metric["value"],
                change_text=metric["change_text"],
                is_positive=metric["is_positive"],
                emoji=metric.get("emoji", ""),
            )
