import streamlit as st
import pandas as pd
import numpy as np
from src.design import markup
from src.utils.data_loader import load_ui_config, load_simulator_data


def _build_churn_compare_histogram(
    current_pct: float,
    simulated_pct: float,
    *,
    rng_seed: int = 42,
    n_samples: int = 2000,
    sigma: float = 3.5,
    n_bins: int = 20,
) -> pd.DataFrame:
    """표시용 합성 분포로 구간별 빈도를 만든 뒤 Current / Simulated 비교용 DataFrame을 반환합니다."""
    rng = np.random.default_rng(rng_seed)
    cur = np.clip(rng.normal(float(current_pct), sigma, n_samples), 0.0, 100.0)
    sim = np.clip(rng.normal(float(simulated_pct), sigma, n_samples), 0.0, 100.0)
    bins = np.linspace(0.0, 100.0, n_bins + 1)
    h_cur, edges = np.histogram(cur, bins=bins)
    h_sim, _ = np.histogram(sim, bins=bins)
    labels = [f"{int(edges[i])}-{int(edges[i + 1])}" for i in range(len(edges) - 1)]
    return pd.DataFrame({"Current": h_cur, "Simulated": h_sim}, index=labels)


def render_analysis():
    """고객 분석 및 이탈 시뮬레이터 통합 화면을 렌더링합니다."""
    ui_config = load_ui_config()
    analysis_config = ui_config["analysis"]
    header_config = analysis_config["header"]
    selection_config = analysis_config["customer_selection"]
    form_config = analysis_config["form"]
    chart_copy = analysis_config.get(
        "churn_compare_chart",
        {
            "title": "이탈률 분포 비교",
            "caption": "",
        },
    )
    compare_cfg = analysis_config.get(
        "compare_cards",
        {
            "kpi_current_label": "현재 예상 이탈율",
            "kpi_simulated_label": "시뮬레이션 이탈율",
            "badge_current": "Current",
        },
    )
    ai_cfg = analysis_config.get(
        "ai_comment",
        {
            "title": "AI 분석 코멘트",
            "risk_high": "이탈 위험도가 상승했습니다. 즉각적인 개입이 필요합니다.",
            "risk_low": "안정적인 구독 유지 상태를 보여줍니다.",
            "summary_template": (
                "선택하신 <strong>{segment}</strong> 세그먼트에 대해 조정된 파라미터로 분석한 결과, "
                "이탈율이 <strong>{projected}</strong> 로 예측됩니다."
            ),
        },
    )

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
        st.html(
            markup.analysis_form_section_title(
                form_config.get("section_icon", "tune"),
                form_config["title"],
            )
        )

        with st.form("simulator_form"):
            def_sub_type = selected_row["subscription_type"]
            sub_idx = (
                form_config["subscription_type_options"].index(def_sub_type)
                if def_sub_type in form_config["subscription_type_options"]
                else 0
            )

            subscription_type = st.selectbox(
                form_config["subscription_type_label"],
                form_config["subscription_type_options"],
                index=sub_idx,
            )

            monthly_revenue = st.number_input(
                form_config["monthly_revenue_label"],
                min_value=0.0,
                value=float(selected_row["monthly_revenue"]),
                step=1.0,
            )

            viewing_hours = st.slider(
                form_config["viewing_hours_label"],
                min_value=0.0,
                max_value=200.0,
                value=float(selected_row["viewing_hours"]),
                step=0.5,
            )

            support_calls = st.slider(
                form_config["customer_support_calls_label"],
                min_value=0,
                max_value=20,
                value=int(selected_row["customer_support_calls"]),
                step=1,
            )

            st.html(markup.spacer_height("1rem"))
            submit_button = st.form_submit_button(
                label=form_config["button_label"], type="primary", use_container_width=True
            )

    with col2:
        st.html(markup.spacer_height("2.25rem"))

        if submit_button:
            calc_prob = base_churn_prob

            if def_sub_type != subscription_type:
                if subscription_type == "Premium":
                    calc_prob -= 3.0
                elif subscription_type == "Basic":
                    calc_prob += 5.0
                else:
                    calc_prob += 1.0

            hours_diff = viewing_hours - float(selected_row["viewing_hours"])
            calc_prob -= hours_diff / 10.0

            calls_diff = support_calls - int(selected_row["customer_support_calls"])
            calc_prob += calls_diff * 5.0

            projected_prob = max(1.0, min(99.0, calc_prob))
            projected_prob = round(projected_prob, 1)
        else:
            projected_prob = base_churn_prob

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

        df_hist = _build_churn_compare_histogram(current_prob, projected_prob)
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
