# Python 3.13 이상의 공식 이미지를 기반으로 설정 가능
FROM python:3.13-slim

# MySQL client 빌드를 위한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 스케줄링이나 단발성 실행 방법에 따라 CMD 설정 변경 (임시 뼈대)
CMD ["python", "extract_data.py"]