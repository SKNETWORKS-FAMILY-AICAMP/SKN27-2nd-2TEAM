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
    """폼 제출 여부와 위젯 값."""

    submit: bool
    subscription_type: str
    primary_device: str
    household_size: float | None  # 변경하지 않으면 None


def _resolve_default_index(value: str, options: list[str]) -> int:
    """값을 options의 인덱스로 변환해 selectbox 초기값으로 사용합니다."""
    return options.index(value) if value in options else 0


def _render_subscription_fields(
    selected_row: pd.Series,
    form_config: dict,
) -> tuple[str, str]:
    """요금제 및 주기기 입력 위젯을 렌더링하고 값을 반환합니다."""
    # 요금제
    sub_options = form_config["subscription_type_options"]
    sub_default = str(selected_row.get("subscription_type", "dontcare"))
    sub_index = _resolve_default_index(sub_default, sub_options)
    
    subscription_type = st.selectbox(
        form_config["subscription_type_label"],
        sub_options,
        index=sub_index,
    )
    
    # 주기기
    dev_options = form_config.get("primary_device_options", ["dontcare"])
    dev_default = str(selected_row.get("primary_device", "dontcare"))
    dev_index = _resolve_default_index(dev_default, dev_options)
    
    primary_device = st.selectbox(
        form_config.get("primary_device_label", "주 사용 기기"),
        dev_options,
        index=dev_index,
    )
    
    return subscription_type, primary_device


def _render_behavior_fields(selected_row: pd.Series, form_config: dict) -> float | None:
    """가구원 수 슬라이더를 렌더링하고 값을 반환합니다. (체크박스로 활성화)"""
    use_household_size = st.checkbox(
        form_config.get("household_size_use_label", "가구원 수 변경하기"),
        value=False,
    )
    
    default_hh = float(selected_row.get("household_size", 0.0))
    
    household_size = st.slider(
        form_config.get("household_size_label", "가구원 수 (명)"),
        min_value=0.0,
        max_value=float(form_config.get("household_size_max", 8)),
        value=default_hh,
        step=float(form_config.get("household_size_step", 1.0)),
        disabled=not use_household_size,
    )
    
    if not use_household_size:
        return None
    return float(household_size)


def _read_form_payload(selected_row: pd.Series, form_config: dict) -> SimulatorFormState:
    """폼 내부 위젯 값을 수집해 SimulatorFormState로 묶습니다."""
    subscription_type, primary_device = _render_subscription_fields(selected_row, form_config)
    household_size = _render_behavior_fields(selected_row, form_config)
    
    st.html(markup.spacer_height("1rem"))
    submit_button = st.form_submit_button(
        label=form_config["button_label"],
        type="primary",
        use_container_width=True,
    )
    
    return SimulatorFormState(
        submit=submit_button,
        subscription_type=subscription_type,
        primary_device=primary_device,
        household_size=household_size,
    )


def render_simulator_form(selected_row: pd.Series, form_config: dict) -> SimulatorFormState:
    """섹션 타이틀 + `simulator_form`. 폼 key·위젯 구성은 기존과 동일하게 유지."""
    st.html(
        markup.analysis_form_section_title(
            form_config.get("section_icon", "tune"),
            form_config["title"],
        )
    )
    with st.form("simulator_form"):
        return _read_form_payload(selected_row, form_config)
