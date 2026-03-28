"""
Analysis 라우트 화면: 세그먼트 선택 + 시뮬레이터 폼 + 결과 패널.

- 표시 문구: `ui_config.json`의 `analysis` 블록만 사용
- 폼/휴리스틱: `components.analysis_simulator`, 결과 UI: `components.analysis_outcomes`
- 샘플 행 데이터: `simulator_sample.csv`
"""
import streamlit as st
from src.components.analysis_outcomes import render_analysis_outcomes
from src.components.analysis_simulator import (
    project_churn_probability,
    render_simulator_form,
)
from src.design import markup
from src.utils.data_loader import load_ui_config, load_simulator_data


def render_analysis():
    """고객 분석 및 이탈 시뮬레이터 통합 화면을 렌더링합니다.

    표시 문구는 `ui_config.json`의 `analysis` 블록만 소스로 쓰며, Python에 폴백 문자열을 두지 않습니다.
    """
    ui_config = load_ui_config()
    analysis_config = ui_config["analysis"]
    header_config = analysis_config["header"]
    selection_config = analysis_config["customer_selection"]
    form_config = analysis_config["form"]
    chart_copy = analysis_config["churn_compare_chart"]
    compare_cfg = analysis_config["compare_cards"]
    ai_cfg = analysis_config["ai_comment"]

    df_sample = load_simulator_data()

    st.html(markup.page_header_analysis(header_config["title"], header_config["description"]))

    segment_names = df_sample["segment_name"].tolist()

    selected_segment_name = st.selectbox(
        selection_config["label"],
        options=segment_names,
        index=0,
        help=selection_config["help"],
    )

    st.html(markup.spacer_analysis_segment())

    selected_row = df_sample[df_sample["segment_name"] == selected_segment_name].iloc[0]
    base_churn_prob = float(selected_row["base_churn_prob"])

    col1, col2 = st.columns([4, 8], gap="large")

    with col1:
        form_state = render_simulator_form(selected_row, form_config)

    projected_prob = project_churn_probability(
        base_churn_prob,
        selected_row,
        submitted=form_state.submit,
        subscription_type=form_state.subscription_type,
        viewing_hours=form_state.viewing_hours,
        support_calls=form_state.support_calls,
    )

    with col2:
        render_analysis_outcomes(
            base_churn_prob=base_churn_prob,
            projected_prob=projected_prob,
            selected_segment_name=selected_segment_name,
            compare_cfg=compare_cfg,
            chart_copy=chart_copy,
            ai_cfg=ai_cfg,
        )
