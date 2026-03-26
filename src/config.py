from pathlib import Path

# 프로젝트 루트 경로
BASE_DIR = Path(__file__).resolve().parent.parent

# 데이터 파일 경로
DATA_SAMPLE_PATH = BASE_DIR / "data" / "sample" / "sample_segment.csv"
DATA_SERVER_PATH = BASE_DIR / "data" / "server" / "segment_output.csv"

# 모델 및 전처리 파일 경로
MODEL_PATH = BASE_DIR / "models" / "model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "models" / "preprocessor.pkl"