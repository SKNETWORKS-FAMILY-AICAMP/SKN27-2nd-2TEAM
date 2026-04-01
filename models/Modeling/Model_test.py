from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    roc_curve, auc,
    confusion_matrix, classification_report,
    accuracy_score, precision_score, recall_score, f1_score
)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import reset_seeds
from IPython.display import display
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

# ─────────────────────────────────────────
# 1. 모델 학습
# ─────────────────────────────────────────
def train_models(X, y, cat_cols, args):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=args.random_state, stratify=y
    )

    models = {
        'DecisionTree': DecisionTreeClassifier(random_state=args.random_state),
        'XGBoost'     : XGBClassifier(random_state=args.random_state, eval_metric='logloss'),
        'LightGBM'    : LGBMClassifier(random_state=args.random_state),
        'CatBoost'    : CatBoostClassifier(random_state=args.random_state, verbose=0),
    }

    results = {}
    trained_models = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        results[name] = {
            'accuracy' : round(accuracy_score(y_test, y_pred), 4),
            'roc_auc'  : round(roc_auc_score(y_test, y_prob), 4),
        }
        trained_models[name] = model
        print(f"[{name}] accuracy: {results[name]['accuracy']} | roc_auc: {results[name]['roc_auc']}")

    return results, trained_models



# ─────────────────────────────────────────
# 2. 모델 평가 (Score)
# ─────────────────────────────────────────
def evaluate_model(model,
                enc_tr: pd.DataFrame, y_tr: pd.Series,
                enc_te: pd.DataFrame, y_te: pd.Series) -> tuple:
    """train/test score 및 AUC 출력 후 반환"""

    reset_seeds(42)

    score_tr = model.score(enc_tr, y_tr)
    score_te = model.score(enc_te, y_te)
    print(f'score_tr: {score_tr:.4f} / score_te: {score_te:.4f}')

    # 이탈 확률 및 예측값 계산
    y_prob = model.predict_proba(enc_te)[:, 1]
    y_pred = (y_prob > 0.5).astype(int)

    fpr, tpr, _ = roc_curve(y_te, y_prob, pos_label=1)
    auc_te       = auc(fpr, tpr)
    print(f'model AUC: {auc_te:.4f}')

    return score_tr, score_te, y_prob, y_pred, auc_te


# ─────────────────────────────────────────
# ★ 3. 모델별 평가 결과 표 생성
# ─────────────────────────────────────────
def evaluate_all_models(trained_models: dict, split: dict, enc_tr, enc_te) -> pd.DataFrame:
    """모델별 평가 결과를 표로 출력"""

    y_tr = split['y_tr']
    y_te = split['y_te']

    rows = []
    for name, model in trained_models.items():
        score_tr, score_te, y_prob, y_pred, auc_te = evaluate_model(
            model, enc_tr, y_tr, enc_te, y_te
        )
        rows.append({
            '모델'         : name,
            'Train Score' : round(score_tr, 4),
            'Test Score'  : round(score_te, 4),
            'AUC'         : round(auc_te, 4),
            'Overfitting' : '⚠️ 과적합 의심' if score_tr - score_te > 0.1 else '✅ 양호',
        })

    result_df = pd.DataFrame(rows).set_index('모델')
    print(result_df.to_string())
    return result_df

# ─────────────────────────────────────────
# 4. 예측 결과 분석
# ─────────────────────────────────────────
def predict_churners(enc_te: pd.DataFrame,
                    y_prob: pd.Series, y_pred: pd.Series) -> pd.DataFrame:
    """이탈 예측 결과 DataFrame 생성 및 반환"""

    result_Netflix = enc_te.copy()
    result_Netflix['churn_probability'] = y_prob
    result_Netflix['predicted_churn']   = y_pred

    predicted_churners = result_Netflix[result_Netflix['predicted_churn'] == 1]

    print(f"전체 테스트 회원 수       : {len(result_Netflix)}명")
    print(f"모델이 예측한 이탈 회원 수 : {len(predicted_churners)}명")
    display(predicted_churners.head())

    return predicted_churners 