
# 라이브러리, 의존성 선언 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import easydict
import warnings
import torch
import random
import os
import warnings
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score, confusion_matrix, classification_report
from Data_Preprocessing.load_data import get_args, load_data, preprocess_target
from Data_Preprocessing.merge_data import merge_all_data
from Data_Preprocessing.data_split import split_data
from Data_Preprocessing.cleaning import drop_columns, check_data_info, fill_missing_values
from IPython.display import display
from Data_Preprocessing.outlier_handling import detect_outliers, plot_outliers
from Data_Preprocessing.encoding import get_encode_cols, encode_features
from Modeling.Model_test import train_models, evaluate_model,predict_churners, evaluate_all_models
from Modeling.check import check_before_training
from Modeling.save_model import save_train_test, save_submission, save_results, save_model, summarize_results
from Display_graph.cm_fi_graph import plot_confusion_matrix, get_feature_importances
from Display_graph.ac_ls_graph import plot_accuracy_loss

# 실행 함수 
def model_Netflix():

    # 1. 데이터 로드 
    args = get_args()                          # 경로/설정 로드
    data = load_data(args)                     # CSV 데이터 로드

    ori_test = pd.read_csv(args.test_csv)


    plt.style.use('fivethirtyeight')
    plt.ion()

    warnings.filterwarnings('ignore')
    
    # 2. 데이터 병합
    Netflix = data['user'].copy()

    # 3. 로드한 데이터 확인
    print(f'Netflix_users shape: {Netflix.shape}')
    print(f'Netflix_users columns:\n{Netflix.columns.tolist()}')

    # 4. feature, target 분리
    print(f'Netflix columns:\n{Netflix.columns.tolist()}')

    split  = split_data(Netflix, ori_test)
    X_tr   = split['X_tr']
    X_te   = split['X_te']
    y_tr   = split['y_tr']
    y_te   = split['y_te']
    train  = split['train']
    test   = split['test']
    ori_te = split['ori_te']

    # 5. 로드한 데이터에서 결측치 있는지 체크
    check_data_info(Netflix)
    test_user_id = drop_columns(train, test, ori_te)
    fill_missing_values(train, test, ori_te)

    # 6. 이상치 확인
    df_outlier_summary = detect_outliers(train)
    display(df_outlier_summary)
    plot_outliers(train)

    # 7. 인코딩 (숫자 아닌 컬럼 -> 숫자로 변경)
    enc_cols, normal_cols       = get_encode_cols(train)
    print(train.dtypes[train.dtypes == 'object'])
    enc_tr, enc_te, encoder     = encode_features(train, test, enc_cols, normal_cols)

    # 8. 모델 학습 전 데이터 검증
    check_before_training(enc_tr, enc_te)

    # 9. 모델 학습 및 평가
    cat_cols = []  # 이미 인코딩 완료했으므로 빈 리스트
    results, trained_models = train_models(enc_tr, y_tr, cat_cols, args)
    result_df = evaluate_all_models(trained_models, split, enc_tr, enc_te)
    
    # best 모델로 최종 예측
    best_model_name = result_df['AUC'].idxmax()
    best_model = trained_models[best_model_name]
    print(f'Best model: {best_model_name}')

    score_tr, score_te, y_prob, y_pred, auc_te = evaluate_model(best_model, enc_tr, y_tr, enc_te, y_te)
    predicted_churners = predict_churners(enc_te, y_prob, y_pred)

    # 10. 모델/결과 저장 

    save_train_test(args, X_tr, X_te)
    save_model(args, best_model)
    submission_Netflix = save_submission(args, test_user_id, best_model, enc_te)  # 수정
    results = save_results(args, y_te, y_pred, auc_te)
    Netflix_results    = summarize_results(args)



    # 11. 결과 표시 / 시각화

    # 정확도 확인 
    plot_accuracy_loss(results)

    # Confusion matrix 시각화 
    plot_confusion_matrix(y_te, y_pred)

    # feature 중요도
    df_feature_importances = get_feature_importances(best_model, enc_tr, top_n=10)

    input('엔터를 누르면 종료') 

if __name__ == '__main__':
    model_Netflix()