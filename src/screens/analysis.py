"""
Analysis 라우트 화면: 세그먼트 선택 + 시뮬레이터 폼 + 결과 패널.

- 표시 문구: `ui_config.json`의 `analysis` 블록만 사용
- 폼/휴리스틱: `components.analysis_simulator`, 결과 UI: `components.analysis_outcomes`
- 샘플 행 데이터: `simulator_sample.csv`
"""
import streamlit as st
from src.components.analysis_outcomes import render_analysis_outcomes
from src.components.analysis_simulator import render_simulator_form
from src.design import markup
from src.utils.data_loader import (
    load_simulator_data,
    load_simulator_source_users,
    load_ui_config,
)
from src.utils.model_inference import infer_segment_current_and_projected_prob


def _load_analysis_page_config(ui_config: dict) -> dict:
    """analysis 섹션에서 화면 렌더에 필요한 설정만 추려 반환합니다."""
    analysis_config = ui_config["analysis"]
    return {
        "header": analysis_config["header"],
        "selection": analysis_config["customer_selection"],
        "form": analysis_config["form"],
        "layout": analysis_config["layout"],
        "thresholds": analysis_config["thresholds"],
        "heuristics": analysis_config["simulator_heuristics"],
        "chart_copy": analysis_config["churn_compare_chart"],
        "compare_cards": analysis_config["compare_cards"],
        "ai_comment": analysis_config["ai_comment"],
    }


def _resolve_selected_segment(df_sample, selection_config: dict):
    """세그먼트 선택 UI를 렌더링하고 선택된 행(단일)을 반환합니다."""
    segment_names = df_sample["segment_name"].tolist()
    selected_segment_name = st.selectbox(
        selection_config["label"],
        options=segment_names,
        index=0,
        help=selection_config["help"],
    )
    selected_row = df_sample[df_sample["segment_name"] == selected_segment_name].iloc[0]
    return selected_segment_name, selected_row


def _render_analysis_results(
    *,
    col,
    base_churn_prob: float,
    projected_prob: float,
    selected_segment_name: str,
    page_cfg: dict,
) -> None:
    """우측 결과 컬럼(Current/Simulated 카드 + 차트 + AI 요약)을 렌더링합니다."""
    with col:
        render_analysis_outcomes(
            base_churn_prob=base_churn_prob,
            projected_prob=projected_prob,
            selected_segment_name=selected_segment_name,
            compare_cfg=page_cfg["compare_cards"],
            chart_copy=page_cfg["chart_copy"],
            ai_cfg=page_cfg["ai_comment"],
            layout_cfg=page_cfg["layout"],
            thresholds_cfg=page_cfg["thresholds"],
        )


def render_analysis():
    """고객 분석 및 이탈 시뮬레이터 통합 화면을 렌더링합니다.

    표시 문구는 `ui_config.json`의 `analysis` 블록만 소스로 쓰며, Python에 폴백 문자열을 두지 않습니다.
    """
    # 1) 화면 설정/데이터 준비
    ui_config = load_ui_config()
    page_cfg = _load_analysis_page_config(ui_config)
    header_config = page_cfg["header"]
    selection_config = page_cfg["selection"]
    form_config = page_cfg["form"]

    df_sample = load_simulator_data()
    users_df = load_simulator_source_users()

    # 2) 헤더 + 세그먼트 선택
    st.html(markup.page_header_analysis(header_config["title"], header_config["description"]))

    selected_segment_name, selected_row = _resolve_selected_segment(df_sample, selection_config)

    st.html(markup.spacer_analysis_segment())

    col1, col2 = st.columns(page_cfg["layout"]["columns"], gap=page_cfg["layout"]["gap"])

    # 3) 좌측 입력 폼 / 우측 결과 패널
    with col1:
        form_state = render_simulator_form(selected_row, form_config)

    try:
        current_prob, projected_prob, _ = infer_segment_current_and_projected_prob(
            users_df,
            selected_segment_name=selected_segment_name,
            submitted=form_state.submit,
            subscription_type=form_state.subscription_type,
            monthly_revenue=form_state.monthly_revenue,
            viewing_hours=form_state.viewing_hours,
            support_calls=form_state.support_calls,
        )
    except Exception as exc:
        st.error(f"모델 추론 중 오류가 발생했습니다: {exc}")
        return

    _render_analysis_results(
        col=col2,
        base_churn_prob=current_prob,
        projected_prob=projected_prob,
        selected_segment_name=selected_segment_name,
        page_cfg=page_cfg,
    )
