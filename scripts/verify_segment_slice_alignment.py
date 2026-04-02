"""
`simulator_sample.csv`의 segment_size가 `_assign_segment_key` 집계와 일치하는지 검증합니다.

저장소 루트에서:
  python scripts/verify_segment_slice_alignment.py
  python scripts/verify_segment_slice_alignment.py --users data/sample/preprocessed_users.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config.config import BASE_DIR, SIMULATOR_DATA_PATH
from src.utils.model_inference import (
    SEG_GENERAL,
    SEG_LARGE_HOUSEHOLD,
    SEG_LONG_TERM,
    SEG_MOBILE,
    SEG_PREMIUM,
    _assign_segment_key,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--users",
        type=Path,
        default=BASE_DIR / "data" / "sample" / "preprocessed_users.csv",
        help="전처리된 사용자 CSV (subscription_plan, primary_device, household_size, start_year 포함)",
    )
    args = parser.parse_args()

    users = pd.read_csv(args.users)
    required = ("subscription_plan", "primary_device", "household_size", "start_year")
    missing = [c for c in required if c not in users.columns]
    if missing:
        print(f"[fail] 필수 컬럼 없음: {missing}")
        sys.exit(1)

    keys = _assign_segment_key(users)
    actual = keys.value_counts()

    sample = pd.read_csv(SIMULATOR_DATA_PATH)
    key_by_prefix = {
        "프리미엄_가입군": SEG_PREMIUM,
        "모바일_주사용군": SEG_MOBILE,
        "다인가구군": SEG_LARGE_HOUSEHOLD,
        "장기가입군": SEG_LONG_TERM,
        "일반_안정군": SEG_GENERAL,
    }
    ok = True
    for _, row in sample.iterrows():
        name = str(row["segment_name"])
        expected_n = int(row["segment_size"])
        label = next((v for p, v in key_by_prefix.items() if name.startswith(p)), None)
        if label is None:
            print(f"[fail] 알 수 없는 segment_name 접두어: {name[:50]}...")
            ok = False
            continue
        got = int(actual.get(label, 0))
        if got != expected_n:
            print(f"[fail] {label}: CSV segment_size={expected_n}, 실제={got}")
            ok = False
        else:
            print(f"[ok] {label}: {got}")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
