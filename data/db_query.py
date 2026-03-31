import sys
import os

# 파일 디렉토리 확인
current_dir = os.path.dirname(os.path.abspath(__file__))

# 백앤드 패스 찾아서 경로로 결합 
backend_path = os.path.abspath(os.path.join(current_dir, "..", "backend"))

# 시스템 패스 찾아봐서 없으면 추가 
if backend_path not in sys.path:
    sys.path.append(backend_path)

from extract_data import get_data_from_db

# 로컬 테스트를 위해 부모 디렉토리의 .env 파일을 찾아 수동으로 환경변수 세팅
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

query = "SELECT * FROM users"
print(get_data_from_db(query))

