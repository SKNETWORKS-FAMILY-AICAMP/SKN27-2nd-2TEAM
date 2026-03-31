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
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, r2_score, confusion_matrix, classification_report
from models.Data_Preprocessing.load_data import get_args, load_data, preprocess_target
from models.Data_Preprocessing.merge_data import merge_all_data
from models.Data_Preprocessing.data_split import split_data
from models.Data_Preprocessing.cleaning import drop_columns, check_data_info, fill_missing_values
from IPython.display import display
from models.Data_Preprocessing.outlier_handling import detect_outliers, plot_outliers
from models.Data_Preprocessing.encoding import get_encode_cols, encode_features
from models.Modeling.train_test import train_model, evaluate_model,predict_churners
from models.Modeling.check import check_before_training
from models.Modeling.save_model import save_train_test, save_submission, save_results, save_model, summarize_results
from models.Display_graph.cm_fi_graph import plot_confusion_matrix, get_feature_importances
from models.Display_graph.ac_ls_graph import plot_accuracy_loss

########################################################

def main():

    # 1. 데이터 로드 
    args          = get_args()                          # 경로/설정 로드
    data          = load_data(args)                     # CSV 데이터 로드
    Netflix_users = preprocess_target(data['user'])     # 타겟 변환


    ori_train = pd.read_csv(args.train_csv)
    ori_test = pd.read_csv(args.test_csv)
    pd.read_csv(args.default_submission_csv).shape
    
    # 2. 데이터 병합
    Netflix = merge_all_data(
        user        = data['user'],
        watch       = data['watch'],
        movies      = data['movies'],
        rec_logs    = data['rec_logs'],
        search_logs = data['search_logs'],
        reviews     = data['reviews']
    )

    # 3. 로드한 데이터 확인
    print(f'{ori_train.shape, ori_test.shape}')
    print(f'{Netflix.head()}')    

    # 4. feature, target 분리
    print(f'Netflix columns:\n{Netflix.columns.tolist()}')

    split  = split_data(Netflix_users, ori_test)
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


    df_outlier_summary = detect_outliers(train)
    display(df_outlier_summary)
    plot_outliers(train)

    # 6. 인코딩 (숫자 아닌 컬럼 -> 숫자로 변경)
    enc_cols, normal_cols       = get_encode_cols(train)
    enc_tr, enc_te, encoder     = encode_features(train, test, enc_cols, normal_cols)

    # 7. 모델 학습 전 데이터 검증
    check_before_training(enc_tr, enc_te)

    # 8. 모델 학습 및 평가
    model = train_model(enc_tr, y_tr)
    score_tr, score_te, y_prob, y_pred, auc_te = evaluate_model(model, enc_tr, y_tr, enc_te, y_te)
    predicted_churners = predict_churners(enc_te, y_prob, y_pred)

    # 9. train/test 샘플 데이터 저장
    target_col = y_tr.name if hasattr(y_tr, "name") and y_tr.name else "is_churned"
    if isinstance(y_tr, pd.DataFrame):
        target_col = y_tr.columns[0]
        train_with_target = pd.concat([X_tr.reset_index(drop=True), y_tr.iloc[:, 0].reset_index(drop=True)], axis=1)
    else:
        train_with_target = pd.concat([X_tr.reset_index(drop=True), y_tr.reset_index(drop=True)], axis=1)
    train_with_target = train_with_target.rename(columns={train_with_target.columns[-1]: target_col})
    train_with_target["split"] = "train"

    if isinstance(y_te, pd.DataFrame):
        test_with_target = pd.concat([X_te.reset_index(drop=True), y_te.iloc[:, 0].reset_index(drop=True)], axis=1)
    else:
        test_with_target = pd.concat([X_te.reset_index(drop=True), y_te.reset_index(drop=True)], axis=1)
    test_with_target = test_with_target.rename(columns={test_with_target.columns[-1]: target_col})
    test_with_target["split"] = "test"

    prepared_users = pd.concat([train_with_target, test_with_target], axis=0, ignore_index=True)
    sample_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "sample", "netflix_user.csv")
    prepared_users.to_csv(sample_path, index=False, encoding="utf-8-sig")
    print(f"Saved merged train/test user data to: {sample_path}")



if __name__ == "__main__":
    main()  