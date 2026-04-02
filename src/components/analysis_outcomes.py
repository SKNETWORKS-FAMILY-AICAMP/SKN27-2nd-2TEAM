"""
분석 화면 우열 결과 패널.

- Current vs Simulated KPI 카드 (`ui_config.analysis.compare_cards`)
- 연령 구간별 모델 예측 이탈 인원 막대 그래프 (`churn_compare_chart`, proba 기준)
- AI 요약 카드 (`analysis.ai_comment`)
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.design import markup
from src.design.common import COLORS
from src.utils.analysis_comparison_boxplot import make_churn_comparison_boxplot_figure


def _build_delta_view_model(current_prob: float, projected_prob: float) -> dict:
    """델타 표시용 아이콘·색상·문구 모델."""
    # projected - current: 양수면 악화(이탈률 증가), 음수면 개선.
    prob_delta = projected_prob - current_prob
    is_improved = prob_delta <= 0
    return {
        "prob_delta": prob_delta,
        "trend_icon": "trending_down" if is_improved else "trending_up",
        "delta_color": COLORS["success"] if is_improved else COLORS["danger"],
        "delta_bg": COLORS["success_light"] if is_improved else COLORS["primary_light"],
        "delta_text": f"{prob_delta:+.1f}% Delta",
    }


def _render_kpi_compare_row(
    *,
    current_prob: float,
    projected_prob: float,
    compare_cfg: dict,
    delta_vm: dict,
) -> None:
    """Current/Simulated KPI 2열 렌더링."""
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
                trend_icon=delta_vm["trend_icon"],
                delta_text=delta_vm["delta_text"],
                delta_color=delta_vm["delta_color"],
                delta_bg=delta_vm["delta_bg"],
            )
        )


def _render_comparison_chart_section(
    *,
    chart_df: pd.DataFrame,
    chart_copy: dict,
    chart_height_px: int,
) -> None:
    """연령 구간별 모델 예측 이탈(proba) 인원 수(막대 2색)."""
    title = chart_copy["title"]
    caption = chart_copy.get("caption", "")
    x_label = chart_copy["x_label"]

    fig = make_churn_comparison_boxplot_figure(
        chart_df,
        legend_current=chart_copy["legend_current"],
        legend_simulated=chart_copy["legend_simulated"],
        x_label=x_label,
        y_label=chart_copy["y_label"],
        chart_height_px=chart_height_px,
    )
    with st.container(border=True):
        st.markdown(f"**{title}**")
        if caption:
            st.caption(caption)
        st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _render_ai_summary_section(
    *,
    projected_prob: float,
    selected_segment_name: str,
    ai_cfg: dict,
    high_risk_threshold: float,
) -> None:
    """AI 코멘트 카드 렌더링."""
    # 임계값 초과 여부에 따라 고위험/저위험 문구를 분기.
    is_high_risk = projected_prob > high_risk_threshold
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


def render_analysis_outcomes(
    *,
    base_churn_prob: float,
    projected_prob: float,
    chart_df: pd.DataFrame,
    selected_segment_name: str,
    compare_cfg: dict,
    chart_copy: dict,
    ai_cfg: dict,
    layout_cfg: dict,
    thresholds_cfg: dict,
) -> None:
    """우측 열 전체: 스페이서, KPI 2칸, 박스플롯, AI 요약."""
    st.html(markup.spacer_height(layout_cfg["results_top_spacer"]))
    delta_vm = _build_delta_view_model(base_churn_prob, projected_prob)
    _render_kpi_compare_row(
        current_prob=base_churn_prob,
        projected_prob=projected_prob,
        compare_cfg=compare_cfg,
        delta_vm=delta_vm,
    )
    st.html(markup.spacer_height(layout_cfg["results_section_spacer"]))
    _render_comparison_chart_section(
        chart_df=chart_df,
        chart_copy=chart_copy,
        chart_height_px=int(layout_cfg["histogram_height"]),
    )
    st.html(markup.spacer_height(layout_cfg["results_section_spacer"]))
    _render_ai_summary_section(
        projected_prob=projected_prob,
        selected_segment_name=selected_segment_name,
        ai_cfg=ai_cfg,
        high_risk_threshold=thresholds_cfg["high_risk_churn_prob"],
    )
