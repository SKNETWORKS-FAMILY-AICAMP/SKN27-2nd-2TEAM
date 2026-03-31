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


# ─────────────────────────────────────────
# 1. 모델 학습
# ─────────────────────────────────────────
def train_model(enc_tr: pd.DataFrame, y_tr: pd.Series) -> DecisionTreeClassifier:
    """DecisionTreeClassifier 학습 후 모델 반환"""

    reset_seeds(42)

    model = DecisionTreeClassifier()

    print(f'{enc_tr.shape} / {y_tr.shape}')
    model.fit(enc_tr, y_tr)

    return model


# ─────────────────────────────────────────
# 2. 모델 평가 (Score)
# ─────────────────────────────────────────
def evaluate_model(model: DecisionTreeClassifier,
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
# 3. 예측 결과 분석
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