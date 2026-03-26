# Python 3.9 이상의 공식 이미지를 기반으로 설정 가능
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 스케줄링이나 단발성 실행 방법에 따라 CMD 설정 변경 (임시 뼈대)
CMD ["python", "extract_data.py"]