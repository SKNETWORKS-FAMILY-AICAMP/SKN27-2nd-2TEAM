"""
분석 화면: 연령 구간별 막대 그래프(현재 vs 시뮬, 색 구분).

Streamlit/UI에 의존하지 않음. 소비처: `components.analysis_outcomes`의 `st.pyplot`.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import koreanize_matplotlib  # noqa: F401 — 한글 레이블·범례 폰트 및 마이너스 기호
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from src.design.common import COLORS

# 10세 단위 구간 + 상한 (100세 초과 흡수)
_AGE_BIN_EDGES = [0] + list(range(10, 101, 10)) + [150]
_AGE_BIN_LABELS = [
    "0-9",
    "10-19",
    "20-29",
    "30-39",
    "40-49",
    "50-59",
    "60-69",
    "70-79",
    "80-89",
    "90-99",
    "100+",
]


def _assign_age_bins(chart_df: pd.DataFrame) -> pd.DataFrame:
    """age → age_bin 이 붙은 프레임(유효 행만)."""
    if "age" not in chart_df.columns:
        return pd.DataFrame()
    base = chart_df.copy()
    base["age"] = pd.to_numeric(base["age"], errors="coerce")
    base = base.dropna(subset=["age"])
    if base.empty:
        return pd.DataFrame()
    base["age_bin"] = pd.cut(
        base["age"].to_numpy(dtype=np.float64),
        bins=_AGE_BIN_EDGES,
        labels=_AGE_BIN_LABELS,
        include_lowest=True,
        right=False,
        ordered=True,
    )
    return base.dropna(subset=["age_bin"])


def _predicted_churn_mask(sub: pd.DataFrame, *, pct_col: str, raw_col: str) -> pd.Series:
    """
    실제 레이블(`churned`)은 쓰지 않고, 모델 예측 확률만으로 이탈 여부를 둡니다.
    `proba_churn_raw_*`가 있으면 P(이탈) > 0.5, 없으면 `*_pct` > 50(퍼센트 스케일).
    """
    if raw_col in sub.columns:
        p = pd.to_numeric(sub[raw_col], errors="coerce")
        return p > 0.5
    if pct_col in sub.columns:
        v = pd.to_numeric(sub[pct_col], errors="coerce")
        return v > 50.0
    return pd.Series(False, index=sub.index)


def make_churn_comparison_boxplot_figure(
    chart_df: pd.DataFrame,
    *,
    legend_current: str,
    legend_simulated: str,
    x_label: str,
    y_label: str,
    chart_height_px: int,
) -> Figure:
    """
    연령 구간별 **모델이 이탈로 예측한 인원 수**(proba 기준, 레이블 `churned` 미사용)를
    현재·시뮬 예측 각각 막대로 표시합니다.
    """
    if chart_df.empty or "age" not in chart_df.columns:
        h_in = max(3.0, float(chart_height_px) / 100.0)
        fig, ax = plt.subplots(figsize=(9, h_in), dpi=100)
        ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
        ax.set_axis_off()
        return fig

    with_bins = _assign_age_bins(chart_df)
    if with_bins.empty:
        h_in = max(3.0, float(chart_height_px) / 100.0)
        fig, ax = plt.subplots(figsize=(9, h_in), dpi=100)
        ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
        ax.set_axis_off()
        return fig

    can_cur = "current_pct" in with_bins.columns or "proba_churn_raw_current" in with_bins.columns
    can_sim = "projected_pct" in with_bins.columns or "proba_churn_raw_projected" in with_bins.columns
    rows: list[dict] = []
    for lbl in _AGE_BIN_LABELS:
        sub = with_bins[with_bins["age_bin"].astype(str) == lbl]
        if sub.empty:
            continue
        if can_cur and can_sim:
            n_cur = int(_predicted_churn_mask(sub, pct_col="current_pct", raw_col="proba_churn_raw_current").sum())
            n_sim = int(
                _predicted_churn_mask(sub, pct_col="projected_pct", raw_col="proba_churn_raw_projected").sum()
            )
        else:
            n = int(len(sub))
            n_cur, n_sim = n, n
        rows.append({"age_bin": lbl, "phase": legend_current, "n": n_cur})
        rows.append({"age_bin": lbl, "phase": legend_simulated, "n": n_sim})

    if not rows:
        h_in = max(3.0, float(chart_height_px) / 100.0)
        fig, ax = plt.subplots(figsize=(9, h_in), dpi=100)
        ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
        ax.set_axis_off()
        return fig

    long_df = pd.DataFrame(rows)
    cat_order = [lbl for lbl in _AGE_BIN_LABELS if lbl in long_df["age_bin"].unique()]

    h_in = max(3.0, float(chart_height_px) / 100.0)
    fig, ax = plt.subplots(figsize=(9, h_in), dpi=100)
    sns.barplot(
        data=long_df,
        x="age_bin",
        y="n",
        hue="phase",
        order=cat_order,
        hue_order=[legend_current, legend_simulated],
        palette=[COLORS["secondary"], COLORS["primary"]],
        ax=ax,
    )
    ax.set_xlabel(x_label, color=COLORS["text_main"])
    ax.set_ylabel(y_label, color=COLORS["text_main"])
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(bottom=0.0)
    ax.grid(True, axis="y", alpha=0.25, color=COLORS["border"])
    ax.legend(title="", framealpha=0.9, loc="upper right")
    fig.patch.set_facecolor(COLORS["surface"])
    ax.set_facecolor(COLORS["surface"])
    for spine in ax.spines.values():
        spine.set_color(COLORS["border"])
    fig.tight_layout()
    return fig
