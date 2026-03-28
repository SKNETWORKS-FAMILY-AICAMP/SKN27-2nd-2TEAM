import streamlit as st
import pandas as pd
import numpy as np
from src.utils.data_loader import load_ui_config, load_simulator_data
from src.design.common import COLORS


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

    # 데이터 로드
    df_sample = load_simulator_data()

    # 페이지 헤더
    header_html = f"""
        <div class="page-header">
            <h2 class="page-title">
                <span class="material-symbols-outlined" style="font-size: 2rem; color: {COLORS['primary']};">analytics</span>
                {header_config['title']}
            </h2>
            <p class="page-description">
                {header_config['description']}
            </p>
        </div>
    """
    st.html(header_html)

    # 1. 고객/세그먼트 선택 영역 (상단)
    segment_names = df_sample["segment_name"].tolist()

    selected_segment_name = st.selectbox(
        selection_config["label"],
        options=segment_names,
        index=0,
        help=selection_config["help"],
    )

    st.html('<div class="spacer-2_5" style="height: 1.5rem;"></div>')

    # 선택된 세그먼트 데이터 추출
    selected_row = df_sample[df_sample["segment_name"] == selected_segment_name].iloc[0]
    base_churn_prob = float(selected_row["base_churn_prob"])

    # Bento Grid Layout (4:8 비율)
    col1, col2 = st.columns([4, 8], gap="large")

    with col1:
        st.html(
            f"""
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                <div class="icon-badge primary">
                    <span class="material-symbols-outlined" style="font-size: 1rem;">tune</span>
                </div>
                <h3 style="font-size: 1.125rem; font-weight: 700; margin: 0;">{form_config['title']}</h3>
            </div>
            """
        )

        with st.form("simulator_form"):
            # 기본값 세팅
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

            st.html('<div style="height: 1rem;"></div>')
            submit_button = st.form_submit_button(
                label=form_config["button_label"], type="primary", use_container_width=True
            )

    with col2:
        st.html('<div style="height: 2.25rem;"></div>')

        # 폼 제출 시 혹은 기본적으로 가짜 예측값 생성
        if submit_button:
            # 베이스 확률을 시작점으로 잡고, 변경된 파라미터에 따라 가감 (휴리스틱)
            calc_prob = base_churn_prob

            # 요금제 변경에 따른 효과
            if def_sub_type != subscription_type:
                if subscription_type == "Premium":
                    calc_prob -= 3.0
                elif subscription_type == "Basic":
                    calc_prob += 5.0
                else:
                    calc_prob += 1.0

            # 시청 시간 변화에 따른 효과
            hours_diff = viewing_hours - float(selected_row["viewing_hours"])
            calc_prob -= hours_diff / 10.0

            # 문의 횟수 변화에 따른 효과
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

        # KPI Comparison Cards (축소 타이포)
        res_col1, res_col2 = st.columns(2, gap="medium")

        with res_col1:
            st.html(
                f"""
            <div class="metric-card" style="border-left: 4px solid #e2e8f0; padding: 1rem;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                        <span style="padding: 0.35rem; background-color: #f1f5f9; border-radius: 0.5rem; color: #94a3b8; display: inline-flex; font-size: 1rem;">
                            <span class="material-symbols-outlined" style="font-size: 1.1rem;">trending_flat</span>
                        </span>
                        <span style="font-size: 0.65rem; font-weight: 700; color: #94a3b8; background-color: #f8fafc; padding: 0.2rem 0.45rem; border-radius: 0.25rem;">Current</span>
                    </div>
                    <p style="font-size: 0.55rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 0.15rem 0;">현재 예상 이탈율</p>
                    <p style="font-size: 1.4rem; font-weight: 900; color: #0f172a; margin: 0; line-height: 1.2;">{current_prob}%</p>
                </div>
            </div>
            """
            )

        with res_col2:
            st.html(
                f"""
            <div class="metric-card" style="border-left: 4px solid {COLORS['primary']}; padding: 1rem;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                        <span style="padding: 0.35rem; background-color: {COLORS['primary_light']}; border-radius: 0.5rem; color: {COLORS['primary']}; display: inline-flex;">
                            <span class="material-symbols-outlined" style="font-size: 1.1rem;">{'trending_down' if prob_delta <= 0 else 'trending_up'}</span>
                        </span>
                        <span style="font-size: 0.65rem; font-weight: 700; color: {delta_color}; background-color: {delta_bg}; padding: 0.2rem 0.45rem; border-radius: 0.25rem;">{delta_text}</span>
                    </div>
                    <p style="font-size: 0.55rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 0.15rem 0;">시뮬레이션 이탈율</p>
                    <p style="font-size: 1.4rem; font-weight: 900; color: {COLORS['primary']}; margin: 0; line-height: 1.2;">{projected_prob}%</p>
                </div>
            </div>
            """
            )

        st.html('<div style="height: 1.25rem;"></div>')

        # 이탈률 분포 비교 (히스토그램 빈도 막대)
        df_hist = _build_churn_compare_histogram(current_prob, projected_prob)
        with st.container(border=True):
            st.markdown(f"**{chart_copy['title']}**")
            if chart_copy.get("caption"):
                st.caption(chart_copy["caption"])
            st.bar_chart(df_hist, height=280)

        st.html('<div style="height: 1.25rem;"></div>')

        # Summary Breakdown Section (축소 타이포)
        is_high_risk = projected_prob > 30.0
        risk_color = "#dc2626" if is_high_risk else "#16a34a"
        risk_icon = "warning" if is_high_risk else "check_circle"
        risk_text = (
            "이탈 위험도가 상승했습니다. 즉각적인 개입이 필요합니다."
            if is_high_risk
            else "안정적인 구독 유지 상태를 보여줍니다."
        )

        st.html(
            f"""
        <div class="chart-card" style="padding: 1rem 1.25rem;">
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem;">
                <div class="icon-badge {'primary' if is_high_risk else 'positive'}" style="background-color: {'#fef2f2' if is_high_risk else '#f0fdf4'}; color: {risk_color};">
                    <span class="material-symbols-outlined" style="font-size: 0.95rem;">{risk_icon}</span>
                </div>
                <h3 style="font-size: 0.98rem; font-weight: 700; margin: 0;">AI 분석 코멘트</h3>
            </div>
            <p style="color: #475569; font-size: 0.75rem; line-height: 1.55; margin: 0;">
                선택하신 <strong>{selected_segment_name}</strong> 세그먼트에 대해 조정된 파라미터로 분석한 결과, 이탈율이 <strong>{projected_prob}%</strong> 로 예측됩니다.
                <br><br>
                {risk_text}
            </p>
        </div>
        """
        )
