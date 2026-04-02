# data/db_query.py 실행 가이드 (DB 조회 확인)

## 1) 목적
프론트 작업 중 프로젝트 루트에서 `data/db_query.py`를 실행해 MySQL DB의 `users` 테이블 조회가 정상 동작하는지 확인한다.

## 2) 실행 코드 흐름 요약
- `data/db_query.py`는 `backend` 경로를 `sys.path`에 추가한다.
- 상위 경로의 `.env`를 읽어 환경변수(`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`)를 세팅한다.
- `query = "SELECT * FROM users"`를 실행한다.
- `backend/extract_data.py`의 `get_data_from_db()` -> `get_db_engine()` 순서로 연결 후 `pd.read_sql()`로 조회한다.

## 3) 사전 준비

### 3-1. Python 패키지 설치
프로젝트 루트에서:
```powershell
pip install -r backend/requirements.txt
```

### 3-2. .env 확인
프로젝트 루트의 `.env`에 아래 항목이 있어야 한다.
- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

예시:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=netflix_db
```

참고:
- Docker Compose에서 앱 컨테이너 내부에서 접속할 때는 `DB_HOST=db`
- 로컬(호스트)에서 직접 실행할 때는 보통 `DB_HOST=localhost` 사용

### 3-3. 경로 설정 방식
`data/db_query.py`는 `backend` 경로를 상대경로 기반으로 계산하도록 되어 있다.

```python
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.abspath(os.path.join(current_dir, "..", "backend"))
if backend_path not in sys.path:
    sys.path.append(backend_path)
```

즉, 프로젝트 루트 구조(`data`, `backend`)만 유지되면 로컬 절대경로를 별도로 수정할 필요가 없다.

### 3-4. DB 서버 기동
`docker-compose.yml` 기준으로 DB는 `db` 서비스(MySQL 8.0)이다.
프로젝트 루트에서:
```powershell
docker compose up -d db
```

## 4) 실행 (루트 폴더 기준)

프로젝트 루트에서:
```powershell
python data/db_query.py
```

## 5) 정상 동작 기준
- 콘솔에 `DB 연결 성공` 메시지가 보인다.
- `users` 테이블 조회 결과가 Pandas DataFrame 형태로 출력된다.

## 6) 자주 발생하는 오류와 해결

### A. `ValueError: DB_USER, DB_PASSWORD, DB_NAME ...`
- `.env`에 필수 키가 비어 있거나 누락됨
- `.env` 파일 경로가 프로젝트 루트(`../.env`)에 있는지 확인

### B. `Access denied` / 인증 실패
- `.env`의 계정/비밀번호와 실제 MySQL 설정 불일치
- 컨테이너 재기동 후에도 동일하면 비밀번호/DB명 재확인

### C. `Unknown database` 또는 `Table '...users' doesn't exist`
- DB 또는 `users` 테이블이 아직 생성되지 않음
- 데이터 적재 스크립트(`backend/extract_data.py`) 실행 여부 확인

### D. `ModuleNotFoundError: pymysql` 등
- 의존성 미설치
- `pip install -r backend/requirements.txt` 재실행

## 7) 운영 팁
- 조회 테스트만 할 때는 `SELECT * FROM users LIMIT 10`처럼 제한 쿼리를 권장
- 큰 테이블은 `LIMIT` 없이 조회하면 출력이 과도해질 수 있다
