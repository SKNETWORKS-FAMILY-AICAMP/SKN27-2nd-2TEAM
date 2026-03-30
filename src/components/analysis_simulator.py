"""
분석(이탈 시뮬레이터) 화면 좌열 및 예측 휴리스틱.

- `render_simulator_form`: `ui_config.analysis.form` 기반 `st.form` (키 `simulator_form` 유지)
- `project_churn_probability`: 제출 시 요금제·시청·문의 변화를 반영한 표시용 이탈률(%)
- `SimulatorFormState`: 폼 위젯 값과 제출 여부를 우열 간 전달할 때 사용
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import streamlit as st

from src.design import markup


@dataclass
class SimulatorFormState:
    """폼 제출 여부와 위젯 값 (월 청구액은 현재 휴리스틱에 미반영)."""

    submit: bool
    subscription_type: str
    monthly_revenue: float
    viewing_hours: float
    support_calls: int


def project_churn_probability(
    base_churn_prob: float,
    selected_row: pd.Series,
    *,
    submitted: bool,
    subscription_type: str,
    viewing_hours: float,
    support_calls: int,
) -> float:
    """제출 시 파라미터 변화를 반영한 예측 이탈률(%). 미제출이면 베이스값 그대로."""
    if not submitted:
        return float(base_churn_prob)

    def_sub_type = selected_row["subscription_type"]
    calc_prob = float(base_churn_prob)

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

    calc_prob = max(1.0, min(99.0, calc_prob))
    return round(calc_prob, 1)


def render_simulator_form(selected_row: pd.Series, form_config: dict) -> SimulatorFormState:
    """섹션 타이틀 + `simulator_form`. 폼 key·위젯 구성은 기존과 동일하게 유지."""
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
            label=form_config["button_label"],
            type="primary",
            use_container_width=True,
        )

        return SimulatorFormState(
            submit=submit_button,
            subscription_type=subscription_type,
            monthly_revenue=monthly_revenue,
            viewing_hours=viewing_hours,
            support_calls=support_calls,
        )
