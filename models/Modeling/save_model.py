import json
import joblib
import os
import pandas as pd
from IPython.display import display
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ─────────────────────────────────────────
# 1. train/test 데이터 저장
# ─────────────────────────────────────────
def save_train_test(args, X_tr: pd.DataFrame, X_te: pd.DataFrame) -> None:
    """train/test 데이터를 CSV로 저장"""
    X_tr.to_csv(args.train_csv, index=False)
    X_te.to_csv(args.test_csv, index=False)
    print(f'train 저장 완료: {args.train_csv}')
    print(f'test  저장 완료: {args.test_csv}')


# ─────────────────────────────────────────
# 2. 제출 파일 저장
# ─────────────────────────────────────────
def save_submission(args, X_te: pd.DataFrame,
                    model, enc_te: pd.DataFrame) -> pd.DataFrame:
    """제출용 CSV 생성 및 저장"""
    # 내부 split 결과(X_te)에서 user_id를 꺼내 예측 결과와 함께 저장한다.
    submission_Netflix = X_te[['user_id']].copy()
    submission_Netflix['is_churned'] = model.predict(enc_te)
    submission_Netflix.to_csv(args.default_submission_csv, index=False)
    print(f'제출 파일 저장 완료: {args.default_submission_csv}')
    return submission_Netflix


# ─────────────────────────────────────────
# 3. 모델 평가 지표 저장
# ─────────────────────────────────────────
def save_results(args, y_te: pd.Series, y_pred: pd.Series, auc_te: float) -> dict:
    """모델 평가 지표를 JSON으로 저장 후 반환"""
    accuracy = round(accuracy_score(y_te, y_pred), 4)
    results = {
        "accuracy" : accuracy,
        "loss"     : round(1 - accuracy, 4),
        # 불균형/극단 예측 케이스에서도 예외 없이 지표를 계산한다.
        "precision": round(precision_score(y_te, y_pred, zero_division=0), 4),
        "recall"   : round(recall_score(y_te, y_pred, zero_division=0), 4),
        "f1_score" : round(f1_score(y_te, y_pred, zero_division=0), 4),
        "auc_te"   : round(auc_te, 4)
    }
    args.results.append(results)
    with open(args.save_results, 'w') as file:
        json.dump(results, file, indent=4)
    print(f'결과 저장 완료: {args.save_results}')
    print(json.dumps(results, indent=4))
    return results


# ─────────────────────────────────────────
# 4. 모델 저장                              
# ─────────────────────────────────────────
def save_model(args, model) -> None:
    """학습한 모델을 pkl 파일로 저장"""
    # 오타(Netflex) 파일은 정리하고 Netflix 파일명으로 단일 저장한다.
    save_path = args.default_path + '../model_netflix.pkl'
    legacy_paths = [
        args.default_path + '../model_Netflex.pkl',
        args.default_path + '../model_netflex.pkl',
    ]

    print(f'저장 시도 경로: {save_path}') 

    for old_path in legacy_paths:
        if os.path.exists(old_path):
            os.remove(old_path)
            print(f'기존 파일 삭제: {old_path}')

    joblib.dump(model, save_path)
    print(f'모델 저장 완료: {save_path}')


# ─────────────────────────────────────────
# 5. 전체 결과 요약
# ─────────────────────────────────────────
def summarize_results(args) -> pd.DataFrame:
    """args.results를 AUC 기준 정렬하여 반환"""
    if not args.results:
        print('요약할 결과가 없습니다.')
        return pd.DataFrame()

    Netflix_results = pd.DataFrame(args.results).sort_values(
        by=['auc_te'], ascending=False
    )
    display(Netflix_results)
    return Netflix_results