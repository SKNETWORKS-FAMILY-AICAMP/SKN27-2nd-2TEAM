"""Netflix churn model training pipeline."""

import argparse
import warnings

import matplotlib.pyplot as plt

from Data_Preprocessing.cleaning import (
    check_data_info,
    convert_non_numeric_to_category,
    drop_columns,
    drop_id_like_columns,
    fill_missing_values,
    profile_missing_values,
    split_date_columns,
    validate_before_encoding,
)
from Data_Preprocessing.data_split import split_data
from Data_Preprocessing.encoding import encode_features, get_encode_cols
from Data_Preprocessing.load_data import get_args, load_data, preprocess_target
from Data_Preprocessing.merge_data import merge_all_data
from Data_Preprocessing.outlier_handling import detect_outliers, plot_outliers
from Display_graph.ac_ls_graph import plot_accuracy_loss
from Display_graph.cm_fi_graph import get_feature_importances, plot_confusion_matrix
from IPython.display import display
from Modeling.check import check_before_training
from Modeling.save_model import (
    save_model,
    save_results,
    save_submission,
    save_train_test,
    summarize_results,
)
from Modeling.train_test import evaluate_model, predict_churners, train_model


def model_netflix(encoder_type: str = "hybrid"):
    """users 기준 단일 데이터셋으로 churn 모델을 학습/평가한다."""
    warnings.filterwarnings("ignore")
    plt.style.use("fivethirtyeight")
    plt.ion()

    # 1) 원본 테이블 로드 후 users 타겟(is_churned) 생성
    args = get_args()
    data = load_data(args)
    users_target = preprocess_target(data["user"])

    # 2) users를 기준으로 로그 테이블을 user_id 집계 병합한다.
    netflix = merge_all_data(
        user=users_target,
        watch=data["watch"],
        movies=data["movies"],
        rec_logs=data["rec_logs"],
        search_logs=data["search_logs"],
        reviews=data["reviews"],
    )
    # 병합 직후 원본을 저장해 컬럼별 결측치 전략 수립의 기준 데이터로 사용한다.
    netflix.to_csv(args.netflix_users_csv, index=False)
    print(f"merged user table saved: {args.netflix_users_csv}")
    print(f"users rows: {len(users_target)} / merged rows: {len(netflix)}")
    print(f"netflix columns:\n{netflix.columns.tolist()}")
    print(f"is_churned exists: {'is_churned' in netflix.columns}")
    check_data_info(netflix)
    missing_profile = profile_missing_values(netflix, top_n=40)
    print(f"missing profile rows: {len(missing_profile)}")
    print("top missing columns(before split):")
    print(
        missing_profile[["column", "missing_count", "missing_rate"]]
        .head(10)
        .to_string(index=False)
    )

    # 3) 타겟 기준 8:2(stratify) 분할 후 학습/평가 입력을 준비한다.
    split = split_data(netflix, test_size=0.2, random_state=args.random_state)
    X_tr = split["X_tr"]
    X_te = split["X_te"]
    y_tr = split["y_tr"]
    y_te = split["y_te"]
    train = split["train"]
    test = split["test"]

    # 4) 공통 전처리(불필요 컬럼 제거, 결측치 보정, 이상치 점검)를 수행한다.
    test_user_id = drop_columns(train, test)
    print(f"missing before fill - train: {train.isnull().sum().sum()}, test: {test.isnull().sum().sum()}")
    fill_missing_values(train, test)
    print(f"missing after fill  - train: {train.isnull().sum().sum()}, test: {test.isnull().sum().sum()}")
    for col in ["age", "gender", "monthly_spend", "household_size", "search_clicked_result_position"]:
        if col in train.columns and col in test.columns:
            print(
                f"{col} missing -> train: {train[col].isnull().sum()}, test: {test[col].isnull().sum()}"
            )
    df_outlier_summary = detect_outliers(train)
    display(df_outlier_summary)
    plot_outliers(train)

    # 5) 인코딩 직전 날짜 분해/ID 제거 후 fail-fast 검증을 수행한다.
    split_date_columns(train, test)
    drop_id_like_columns(train, test)
    convert_non_numeric_to_category(train, test)
    validate_before_encoding(train, test)

    # 6) encoder_type(hybrid/onehot/label)에 따라 범주형 인코딩을 수행한다.
    enc_cols, normal_cols = get_encode_cols(train)
    enc_tr, enc_te, encoder = encode_features(
        train, test, enc_cols, normal_cols, encoder_type=encoder_type
    )
    check_before_training(enc_tr, enc_te)

    # 7) 모델 학습/평가와 이탈 예측 결과를 계산한다.
    model = train_model(enc_tr, y_tr)
    score_tr, score_te, y_prob, y_pred, auc_te = evaluate_model(
        model, enc_tr, y_tr, enc_te, y_te
    )
    predicted_churners = predict_churners(enc_te, y_prob, y_pred)
    print(f"submission user_id count: {len(test_user_id)}")
    print(f"predicted churners count: {len(predicted_churners)}")
    print(f"encoder feature count: {len(encoder['feature_names'])}")
    print(f"train/test score: {score_tr:.4f} / {score_te:.4f}")

    # 8) 산출물(분할 데이터, 모델, 지표, 제출 포맷)을 저장한다.
    save_train_test(args, X_tr, X_te)
    save_model(args, model)
    submission_netflix = save_submission(args, X_te, model, enc_te)
    results = save_results(args, y_te, y_pred, auc_te)
    netflix_results = summarize_results(args)
    print(f"submission preview rows: {len(submission_netflix)}")
    print(f"results rows: {len(netflix_results)}")

    # 9) 성능 시각화(정확도/손실, confusion matrix, feature importance)를 출력한다.
    plot_accuracy_loss(results)
    plot_confusion_matrix(y_te, y_pred)
    df_feature_importances = get_feature_importances(model, enc_tr, top_n=10)
    print(df_feature_importances.head(10))

    input("엔터를 누르면 종료")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Netflix churn model training")
    parser.add_argument(
        "--encoder-type",
        default="hybrid",
        choices=["hybrid", "onehot", "label"],
        help="categorical encoder mode",
    )
    cli_args = parser.parse_args()
    model_netflix(encoder_type=cli_args.encoder_type)
