import json
from pathlib import Path

# 프로젝트 루트 경로
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 데이터 파일 경로
DATA_SAMPLE_PATH = BASE_DIR / "data" / "sample" / "sample_segment.csv"

# UI 및 대시보드 데이터 경로
UI_CONFIG_PATH = BASE_DIR / "src" / "config" / "ui_config.json"
KPI_SOURCE_DATA_PATH = BASE_DIR / "data" / "sample" / "netflix_user_sample.csv"
SIMULATOR_DATA_PATH = BASE_DIR / "data" / "sample" / "simulator_sample.csv"
DASHBOARD_MODULES_DATA_PATH = BASE_DIR / "src" / "config" / "dashboard_modules.json"

# 스냅샷(기준일 vs 비교일) 계산 기준 설정
SNAPSHOT_TARGET_MONTH_DAY = "12-25"
SNAPSHOT_DELTA_DAYS = 7
INACTIVE_DAYS_THRESHOLD = 30

# 모델 및 전처리 파일 경로
MODEL_PATH = BASE_DIR / "data" / "model_Netflex.pkl"
PREPROCESSOR_PATH = BASE_DIR / "models" / "preprocessor.pkl"


def load_ui_config_dict() -> dict:
    """UI 설정 JSON 전체를 로드합니다."""
    with open(UI_CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def load_app_shell_config() -> dict:
    """페이지 셸 설정(`ui_config.app`)만 반환합니다."""
    return (load_ui_config_dict().get("app") or {})