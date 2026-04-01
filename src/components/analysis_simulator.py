"""
분석(이탈 시뮬레이터) 화면 좌열 입력 폼.

- `render_simulator_form`: `ui_config.analysis.form` 기반 `st.form` (키 `simulator_form` 유지)
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


def _resolve_subscription_defaults(selected_row: pd.Series, form_config: dict) -> tuple[str, int]:
    """기본 요금제를 options 인덱스로 변환해 selectbox 초기값으로 사용합니다."""
    options = form_config["subscription_type_options"]
    default_value = selected_row["subscription_type"]
    default_index = options.index(default_value) if default_value in options else 0
    return default_value, default_index


def _render_subscription_fields(
    selected_row: pd.Series,
    form_config: dict,
) -> tuple[str, float]:
    """요금제/월 청구액 입력 위젯을 렌더링하고 값을 반환합니다."""
    _, default_index = _resolve_subscription_defaults(selected_row, form_config)
    subscription_type = st.selectbox(
        form_config["subscription_type_label"],
        form_config["subscription_type_options"],
        index=default_index,
    )
    monthly_revenue = st.number_input(
        form_config["monthly_revenue_label"],
        min_value=0.0,
        value=float(selected_row["monthly_revenue"]),
        step=1.0,
    )
    return subscription_type, monthly_revenue


def _render_behavior_fields(selected_row: pd.Series, form_config: dict) -> tuple[float, int]:
    """시청시간/문의횟수 슬라이더를 렌더링하고 값을 반환합니다."""
    viewing_hours = st.slider(
        form_config["viewing_hours_label"],
        min_value=0.0,
        max_value=float(form_config["viewing_hours_max"]),
        value=float(selected_row["viewing_hours"]),
        step=float(form_config["viewing_hours_step"]),
    )
    support_calls = st.slider(
        form_config["customer_support_calls_label"],
        min_value=0,
        max_value=int(form_config["support_calls_max"]),
        value=int(selected_row["customer_support_calls"]),
        step=int(form_config["support_calls_step"]),
    )
    return viewing_hours, support_calls


def _read_form_payload(selected_row: pd.Series, form_config: dict) -> SimulatorFormState:
    """폼 내부 위젯 값을 수집해 SimulatorFormState로 묶습니다."""
    subscription_type, monthly_revenue = _render_subscription_fields(selected_row, form_config)
    viewing_hours, support_calls = _render_behavior_fields(selected_row, form_config)
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


def render_simulator_form(selected_row: pd.Series, form_config: dict) -> SimulatorFormState:
    """섹션 타이틀 + `simulator_form`. 폼 key·위젯 구성은 기존과 동일하게 유지."""
    # 제목(아이콘+텍스트)은 마크업 함수로 렌더링.
    st.html(
        markup.analysis_form_section_title(
            form_config.get("section_icon", "tune"),
            form_config["title"],
        )
    )
    with st.form("simulator_form"):
        return _read_form_payload(selected_row, form_config)
