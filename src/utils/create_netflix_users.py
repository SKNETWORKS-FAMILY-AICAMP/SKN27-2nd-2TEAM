"""
하위 호환 래퍼.

기존 경로(`src/utils/create_netflix_users.py`)를 호출하던 사용자를 위해
실제 구현(`scripts/create_netflix_users.py`)을 재노출합니다.
"""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.create_netflix_users import (
    build_table_paths,
    load_server_data,
    main,
    preprocess_target,
)


if __name__ == "__main__":
    main()