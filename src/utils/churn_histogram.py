"""
이탈률 비교 막대 차트용 데이터: numpy로 합성 분포를 뽑아 구간별 빈도 DataFrame 생성.

Streamlit/UI에 의존하지 않음. 소비처: `components.analysis_outcomes`의 `st.bar_chart`.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def build_churn_compare_histogram(
    current_pct: float,
    simulated_pct: float,
    *,
    rng_seed: int = 42,
    n_samples: int = 2000,
    sigma: float = 3.5,
    n_bins: int = 20,
) -> pd.DataFrame:
    """표시용 합성 분포로 구간별 빈도를 만든 뒤 Current / Simulated 비교용 DataFrame을 반환합니다."""
    # 고정 시드로 실행마다 동일한 분포를 재현해 비교 시각화를 안정화합니다.
    rng = np.random.default_rng(rng_seed)
    # 현재/시뮬레이션 평균을 중심으로 정규분포 샘플을 생성하고 0~100으로 클립합니다.
    cur = np.clip(rng.normal(float(current_pct), sigma, n_samples), 0.0, 100.0)
    sim = np.clip(rng.normal(float(simulated_pct), sigma, n_samples), 0.0, 100.0)
    # 동일 bin 경계로 빈도를 계산해 두 분포를 같은 축에서 비교합니다.
    bins = np.linspace(0.0, 100.0, n_bins + 1)
    h_cur, edges = np.histogram(cur, bins=bins)
    h_sim, _ = np.histogram(sim, bins=bins)
    labels = [f"{int(edges[i])}-{int(edges[i + 1])}" for i in range(len(edges) - 1)]
    return pd.DataFrame({"Current": h_cur, "Simulated": h_sim}, index=labels)
