"""
시뮬레이터와 동일한 추론 파이프라인으로 세그먼트별 변경 전·후 이탈 확률(%)을 CSV로보냅니다.

실행 (저장소 루트에서):
  python scripts/export_simulator_prediction_sample.py
  python scripts/export_simulator_prediction_sample.py --max-rows 2000 --output data/sample/my_export.csv

출력 기본 경로: data/sample/simulator_prediction_before_after.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd

from src.config.config import BASE_DIR, SIMULATOR_DATA_PATH, USERS_SOURCE_DATA_PATH
from src.utils.model_inference import infer_segment_current_and_projected_prob, slice_users_by_segment
from src.utils.preprocess_users_data import preprocess_users_data

DEFAULT_OUT = BASE_DIR / "data" / "sample" / "simulator_prediction_before_after.csv"


def _segment_frame_aligned(users_df: pd.DataFrame, segment_name: str) -> pd.DataFrame:
    """infer 내부와 동일: 슬라이스 후 churned 열 제거."""
    seg = slice_users_by_segment(users_df, segment_name)
    if seg.empty:
        return seg
    if "churned" in seg.columns:
        seg = seg.drop(columns=["churned"])
    return seg


def main() -> None:
    parser = argparse.ArgumentParser(description="시뮬레이터 예측 샘플 CSV보내기")
    parser.add_argument(
        "--max-rows",
        type=int,
        default=800,
        help="세그먼트당 최대 행 수(용량 제한). 0이면 전체.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUT,
        help="출력 CSV 경로",
    )
    args = parser.parse_args()

    users_df = pd.read_csv(USERS_SOURCE_DATA_PATH)
    users_df = preprocess_users_data(users_df)
    sim_rows = pd.read_csv(SIMULATOR_DATA_PATH)

    chunks: list[pd.DataFrame] = []
    for _, row in sim_rows.iterrows():
        seg_name = str(row["segment_name"])
        sub = str(row.get("subscription_plan", row.get("subscription_type", "dontcare")))
        dev = str(row.get("primary_device", "dontcare"))
        hh_raw = row.get("household_size")
        hh = float(hh_raw) if pd.notna(hh_raw) else None

        seg_work = _segment_frame_aligned(users_df, seg_name)
        if seg_work.empty:
            print(f"[skip] 빈 세그먼트: {seg_name}")
            continue

        cur_mean, proj_mean, n_users, _, _, chart_df = infer_segment_current_and_projected_prob(
            users_df,
            selected_segment_name=seg_name,
            submitted=True,
            subscription_plan=sub,
            primary_device=dev,
            household_size=hh,
        )

        export = chart_df.copy()
        export.insert(0, "segment_name", seg_name)
        if "user_id" in seg_work.columns and "user_id" not in export.columns:
            export.insert(1, "user_id", seg_work["user_id"].values)

        export["scenario_subscription_plan"] = sub
        export["scenario_primary_device"] = dev
        export["scenario_household_size"] = hh
        export["segment_mean_current_pct"] = cur_mean
        export["segment_mean_projected_pct"] = proj_mean
        export["segment_user_count"] = n_users

        if "proba_churn_raw_current" in export.columns:
            rc = export["proba_churn_raw_current"]
            print(
                f"    raw P(churn) current: min={rc.min():.6g} max={rc.max():.6g} "
                f"n_unique={rc.nunique()}"
            )

        if args.max_rows > 0 and len(export) > args.max_rows:
            export = export.head(args.max_rows).copy()
            export["export_truncated"] = True
        else:
            export["export_truncated"] = False

        chunks.append(export)
        print(
            f"[ok] {seg_name[:40]}... users={n_users}, "
            f"mean_cur={cur_mean}%, mean_proj={proj_mean}%, exported_rows={len(export)}"
        )

    if not chunks:
        print("보낼 데이터가 없습니다.")
        sys.exit(1)

    out_df = pd.concat(chunks, ignore_index=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"\n저장 완료: {args.output} (총 {len(out_df)}행)")
    print("\ncurrent_pct 요약:")
    print(out_df["current_pct"].describe())
    print("\nprojected_pct 요약:")
    print(out_df["projected_pct"].describe())
    print(f"\ncurrent_pct 고유값 개수(전체): {out_df['current_pct'].nunique()}")
    if "proba_churn_raw_current" in out_df.columns:
        r = out_df["proba_churn_raw_current"]
        print(f"proba_churn_raw_current 고유값 개수: {r.nunique()}")
        print(
            "※ current_pct가 0과 100%만 있어도, predict_proba 기반이 맞을 수 있습니다. "
            "트리/부스팅에서 리프가 순수하면 P(이탈)이 정확히 0 또는 1만 나옵니다."
        )


if __name__ == "__main__":
    main()
