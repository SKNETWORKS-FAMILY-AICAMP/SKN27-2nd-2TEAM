"""
분석 화면 우열 결과 패널.

- Current vs Simulated KPI 카드 (`ui_config.analysis.compare_cards`)
- `build_churn_compare_histogram` + `st.bar_chart` 분포 비교 (`churn_compare_chart`)
- AI 요약 카드 (`analysis.ai_comment`)
"""

from __future__ import annotations

import streamlit as st

from src.design import markup
from src.utils.churn_histogram import build_churn_compare_histogram


def render_analysis_outcomes(
    *,
    base_churn_prob: float,
    projected_prob: float,
    selected_segment_name: str,
    compare_cfg: dict,
    chart_copy: dict,
    ai_cfg: dict,
) -> None:
    """우측 열 전체: 상단 정렬 스페이서, KPI 2칸, 히스토그램, AI 요약."""
    st.html(markup.spacer_height("2.25rem"))

    current_prob = base_churn_prob
    prob_delta = projected_prob - current_prob
    delta_color = "#16a34a" if prob_delta <= 0 else "#dc2626"
    delta_bg = "#f0fdf4" if prob_delta <= 0 else "#fef2f2"
    delta_text = f"{prob_delta:+.1f}% Delta"

    res_col1, res_col2 = st.columns(2, gap="medium")

    with res_col1:
        st.html(
            markup.analysis_kpi_current_card(
                current_prob,
                kpi_label=compare_cfg["kpi_current_label"],
                badge_current=compare_cfg["badge_current"],
            )
        )

    with res_col2:
        st.html(
            markup.analysis_kpi_simulated_card(
                projected_prob,
                kpi_label=compare_cfg["kpi_simulated_label"],
                trend_icon="trending_down" if prob_delta <= 0 else "trending_up",
                delta_text=delta_text,
                delta_color=delta_color,
                delta_bg=delta_bg,
            )
        )

    st.html(markup.spacer_height("1.25rem"))

    df_hist = build_churn_compare_histogram(current_prob, projected_prob)
    with st.container(border=True):
        st.markdown(f"**{chart_copy['title']}**")
        if chart_copy.get("caption"):
            st.caption(chart_copy["caption"])
        st.bar_chart(df_hist, height=280)

    st.html(markup.spacer_height("1.25rem"))

    is_high_risk = projected_prob > 30.0
    risk_text = ai_cfg["risk_high"] if is_high_risk else ai_cfg["risk_low"]

    st.html(
        markup.analysis_ai_comment_card(
            segment_name=selected_segment_name,
            projected_prob=projected_prob,
            risk_text=risk_text,
            title=ai_cfg["title"],
            summary_template=ai_cfg["summary_template"],
            is_high_risk=is_high_risk,
        )
    )
