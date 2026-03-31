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


def _build_delta_view_model(current_prob: float, projected_prob: float) -> dict:
    """델타 표시용 아이콘·색상·문구 모델."""
    # projected - current: 양수면 악화(이탈률 증가), 음수면 개선.
    prob_delta = projected_prob - current_prob
    is_improved = prob_delta <= 0
    return {
        "prob_delta": prob_delta,
        "trend_icon": "trending_down" if is_improved else "trending_up",
        "delta_color": "#16a34a" if is_improved else "#dc2626",
        "delta_bg": "#f0fdf4" if is_improved else "#fef2f2",
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


def _render_histogram_section(
    *,
    current_prob: float,
    projected_prob: float,
    chart_copy: dict,
    histogram_height: int,
) -> None:
    """Current/Simulated 히스토그램 섹션."""
    # 동일 bin 기준으로 두 분포를 비교하기 위한 참고용 데이터프레임.
    df_hist = build_churn_compare_histogram(current_prob, projected_prob)
    with st.container(border=True):
        st.markdown(f"**{chart_copy['title']}**")
        if chart_copy.get("caption"):
            st.caption(chart_copy["caption"])
        st.bar_chart(df_hist, height=histogram_height)


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
    selected_segment_name: str,
    compare_cfg: dict,
    chart_copy: dict,
    ai_cfg: dict,
    layout_cfg: dict,
    thresholds_cfg: dict,
) -> None:
    """우측 열 전체: 스페이서, KPI 2칸, 히스토그램, AI 요약."""
    # 레이아웃 간격/차트 높이/임계값은 모두 설정(ui_config)에서 주입받아 사용.
    st.html(markup.spacer_height(layout_cfg["results_top_spacer"]))
    delta_vm = _build_delta_view_model(base_churn_prob, projected_prob)
    _render_kpi_compare_row(
        current_prob=base_churn_prob,
        projected_prob=projected_prob,
        compare_cfg=compare_cfg,
        delta_vm=delta_vm,
    )
    st.html(markup.spacer_height(layout_cfg["results_section_spacer"]))
    _render_histogram_section(
        current_prob=base_churn_prob,
        projected_prob=projected_prob,
        chart_copy=chart_copy,
        histogram_height=layout_cfg["histogram_height"],
    )
    st.html(markup.spacer_height(layout_cfg["results_section_spacer"]))
    _render_ai_summary_section(
        projected_prob=projected_prob,
        selected_segment_name=selected_segment_name,
        ai_cfg=ai_cfg,
        high_risk_threshold=thresholds_cfg["high_risk_churn_prob"],
    )
