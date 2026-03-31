"""
모델 학습 전 데이터 검증(확인)
1. 학습(train) 데이터셋 컬럼과 평가(test) 데이터셋 컬럼이 동일해야함
2. 학습(train) & 평가(test) 모두 결측치가 없어야 함
3. 학습(train) & 평가(test) 모두 문자열 데이터가 없거나, category로 형변환 되어있어야 함
"""
import pandas as pd
import numpy as np

def check_before_training(train_features:pd.DataFrame, test:pd.DataFrame) -> None:
    if sum(train_features.columns == test.columns) != train_features.shape[1]:
        # 1. 학습(train) 데이터셋 컬럼과 평가(test) 데이터셋 컬럼이 동일해야함
        raise Exception("학습(train) 데이터셋 컬럼과 평가(test) 데이터셋 컬럼이 다름")
    elif (train_features.isnull().sum().sum() + test.isnull().sum().sum()):
        # 2. 학습(train) & 평가(test) 모두 결측치가 없어야 함
        raise Exception("학습(train) & 평가(test) 모두 결측치가 존재")
    elif (not train_features.select_dtypes(exclude=[np.number, 'category']).empty) \
        or (not train_features.select_dtypes(exclude=[np.number, 'category']).empty):
        # 3. 학습(train) & 평가(test) 모두 문자열 데이터가 없거나, category로 형변환 되어있어야 함
        raise Exception("학습(train) & 평가(test) 모두 문자열 데이터가 존재")