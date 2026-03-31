import sys
import os

sys.path.append("../backend")

# 로컬 테스트를 위해 부모 디렉토리의 .env 파일을 찾아 수동으로 환경변수 세팅
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

from extract_data import get_data_from_db

query = "SELECT * FROM users"
print(get_data_from_db(query))

