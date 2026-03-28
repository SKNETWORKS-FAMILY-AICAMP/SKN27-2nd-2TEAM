import streamlit as st
from src.design import markup
from src.utils.data_loader import load_dashboard_modules_data


def render_dashboard_modules():
    """대시보드 하단 3개 모듈 (플랜 분포, 이탈 사유, 최근 세션) 렌더링"""
    data = load_dashboard_modules_data()

    st.html(markup.spacer_std())

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.html(markup.dashboard_plan_module(data["plan_distribution"]))

    with col2:
        st.html(markup.dashboard_churn_reasons_module(data["churn_reasons"]))

    with col3:
        st.html(markup.dashboard_sessions_module(data["recent_sessions"]))
