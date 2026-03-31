# 백엔드(MySQL <-> CSV 파이프라인) 데이터 로드 및 추출
import os
import time
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text

import kagglehub

BASE_DIR = Path(__file__).resolve().parent

def download_data(kaggle_src="sayeeduddin/netflix-2025user-behavior-dataset-210k-records", output_dir=BASE_DIR / "../data" / "raw"):
    """
    Kaggle에서 데이터를 다운로드하는 함수입니다. 도커 컨테이너 내부에 원본 csv 파일을 저장
    
    Args:
        kaggle_src (str): Kaggle 데이터셋의 경로 (예: "sayeeduddin/netflix-2025user-behavior-dataset-210k-records")
        output_dir (str): 데이터를 저장할 로컬 디렉토리 경로
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Downloading dataset from Kaggle: {kaggle_src}")
    kagglehub.dataset_download(kaggle_src, output_dir=output_dir)
    print(f"Dataset downloaded to: {output_dir}")

def preprocess_data(df):
    '''
    # 1차 전처리 함수 설계
    # 1. 중복값을 갖는 행 제거
    # 2. id에 해당되는 컬럼들을 정수형으로 변환
    '''
    df.drop_duplicates(inplace=True)
    for col in df.columns:
        if col.endswith("_id"):
            df[col] = df[col].map(lambda x: int(x.split("_")[1]))
    return df

def get_db_engine(max_retries=10, delay=5):
    """
    환경 변수에서 DB 연결 정보를 읽어 SQLAlchemy 엔진을 생성하는 함수입니다.
    DB가 준비될 때까지 재시도합니다.
    
    Args:
        max_retries (int): 최대 재시도 횟수
        delay (int): 재시도 간격(초)
    
    Returns:
        sqlalchemy.engine.base.Engine: SQLAlchemy 엔진 객체
    """
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME")
    
    if not all([db_user, db_password, db_name]):
        raise ValueError("DB_USER, DB_PASSWORD, DB_NAME 환경 변수가 모두 설정되어야 합니다.")
    
    connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
    
    for attempt in range(max_retries):
        try:
            engine = create_engine(connection_string)
            # 연결 테스트
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("DB 연결 성공")
            return engine
        except Exception as e:
            print(f"DB 연결 실패 (시도 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise e

def load_data_to_db():
    """
    CSV 파일에서 데이터를 읽어 MySQL 데이터베이스에 로드하는 함수입니다.
    """
    download_data()  # Kaggle에서 데이터 다운로드
    engine = get_db_engine()

    data_dir = Path("../data/raw/")
    for csv_file in data_dir.glob("*.csv"):
        table_name = csv_file.stem.lower().replace("-", "_").replace(" ", "_")
        df = pd.read_csv(csv_file)
        proc_df = preprocess_data(df)

        # 데이터베이스에 테이블이 없으면 생성, 있으면 덮어쓰기
        proc_df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print(f"{csv_file.name} -> {table_name} 적재 완료")

def set_schema_to_db():
    """
    데이터베이스 스키마를 설정하는 함수입니다.
    """
    engine = get_db_engine()
    with engine.connect() as conn:
        # 기존에 생성된 테이블 컬럼에 프라이머리 키 설정: user_id, movie_id, reccomendation_id, search_id, review_id, session_id
        conn.execute(text("""
            ALTER TABLE users
            MODIFY COLUMN user_id INT PRIMARY KEY;
        """))
        conn.execute(text("""
            ALTER TABLE movies
            MODIFY COLUMN movie_id INT PRIMARY KEY;
        """))
        conn.execute(text("""
            ALTER TABLE recommendation_logs 
            MODIFY COLUMN recommendation_id INT PRIMARY KEY;
        """))
        conn.execute(text("""
            ALTER TABLE search_logs 
            MODIFY COLUMN search_id INT PRIMARY KEY;
        """))
        conn.execute(text("""
            ALTER TABLE reviews 
            MODIFY COLUMN review_id INT PRIMARY KEY;
        """))
        conn.execute(text("""
            ALTER TABLE watch_history 
            MODIFY COLUMN session_id INT PRIMARY KEY;
        """))

        # Foreign key 설정을 위해 자식 키의 속성 변경(자료형, null 허용 여부) 후, Foreign key 제약 조건 추가
        conn.execute(text("""
            ALTER TABLE search_logs
            MODIFY COLUMN user_id INT not null,
            ADD CONSTRAINT fk_search_user FOREIGN KEY (user_id) REFERENCES users(user_id);
        """))
        conn.execute(text("""
            ALTER TABLE recommendation_logs
            MODIFY COLUMN user_id INT not null,
            MODIFY COLUMN movie_id INT not null,
            ADD CONSTRAINT fk_recommendation_user FOREIGN KEY (user_id) REFERENCES users(user_id),
            ADD CONSTRAINT fk_recommendation_movie FOREIGN KEY (movie_id) REFERENCES movies(movie_id);
        """))
        conn.execute(text("""
            ALTER TABLE reviews
            MODIFY COLUMN user_id INT not null,
            MODIFY COLUMN movie_id INT not null,
            ADD CONSTRAINT fk_review_user FOREIGN KEY (user_id) REFERENCES users(user_id),
            ADD CONSTRAINT fk_review_movie FOREIGN KEY (movie_id) REFERENCES movies(movie_id);
        """))
        conn.execute(text("""
            ALTER TABLE watch_history
            MODIFY COLUMN user_id INT not null,
            MODIFY COLUMN movie_id INT not null,
            ADD CONSTRAINT fk_watch_user FOREIGN KEY (user_id) REFERENCES users(user_id),
            ADD CONSTRAINT fk_watch_movie FOREIGN KEY (movie_id) REFERENCES movies(movie_id);
        """))
        print("스키마 설정 완료")

def get_data_from_db(query, engine=None):
    '''
    pandas를 사용하여 DB에서 데이터를 추출하고 데이터프레임 객체 형태로 반환하는 함수
    '''
    if engine is None:
        engine = get_db_engine()
        
    with engine.connect() as conn:
        data = pd.read_sql(query, conn)

    return data

if __name__ == "__main__":
    load_data_to_db()
    set_schema_to_db()