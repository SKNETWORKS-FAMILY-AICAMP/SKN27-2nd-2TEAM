import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from IPython.display import display

# ─────────────────────────────────────────
# 혼동 행렬 시각화 및 지표 출력
# ─────────────────────────────────────────
def plot_confusion_matrix(y_te: pd.Series, y_pred: pd.Series) -> None:
    """혼동 행렬 시각화 및 파생 지표 출력"""

    # 1. 혼동 행렬 생성
    cm = confusion_matrix(y_te, y_pred)

    # 2. 히트맵 시각화
    plt.figure(figsize=(8, 6))
    sns.set(font_scale=1.2)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Stay (0)', 'Churn (1)'],
                yticklabels=['Stay (0)', 'Churn (1)'])
    plt.xlabel('Predicted (Model)')
    plt.ylabel('Actual (Real)')
    plt.title('Netflix Churn Confusion Matrix')
    plt.show()

    # 3. 혼동 행렬 값 추출
    tn, fp, fn, tp = cm.ravel()

    print("=" * 45)
    print("         혼동 행렬(Confusion Matrix) 해석")
    print("=" * 45)
    print(f"✅ TN (True Negative)  : {tn:>6,}명")
    print(f"   → 유지인데, 모델도 유지로 정확히 예측")
    print()
    print(f"❌ FP (False Positive) : {fp:>6,}명")
    print(f"   → 유지인데, 모델이 이탈로 잘못 예측")
    print()
    print(f"❌ FN (False Negative) : {fn:>6,}명")
    print(f"   → 실제 이탈인데, 모델이 유지로 잘못 예측")
    print()
    print(f"✅ TP (True Positive)  : {tp:>6,}명")
    print(f"   → 실제 이탈인데, 모델도 이탈으로 정확히 예측")
    print("=" * 45)

    # 4. 파생 지표 출력
    accuracy  = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    print(f"\n📊 파생 지표 요약")
    print("=" * 45)
    print(f"  Accuracy  (전체 정확도)     : {accuracy:.4f}  → 전체 중 맞춘 비율")
    print(f"  Precision (정밀도)          : {precision:.4f}  → Churn 예측 중 실제 Churn 비율")
    print(f"  Recall    (재현율)          : {recall:.4f}  → 실제 Churn 중 맞춘 비율")
    print(f"  F1 Score  (정밀도+재현율)   : {f1:.4f}  → Precision과 Recall의 조화 평균")
    print("=" * 45)


# ─────────────────────────────────────────
# 5. 피처 중요도 분석
# ─────────────────────────────────────────
def get_feature_importances(model: DecisionTreeClassifier,
                            enc_tr: pd.DataFrame,
                            top_n: int = 20) -> pd.DataFrame:
    """피처 중요도 DataFrame 생성 및 반환"""

    df_feature_importances = pd.DataFrame(
        model.feature_importances_,
        index=enc_tr.columns,
        columns=['importance']
    ).sort_values(by='importance', ascending=False).reset_index()

    df_feature_importances['importance_%'] = (
        df_feature_importances['importance'] * 100
    ).round(2).astype(str) + '%'

    # 상위 top_n개만 표시
    df_display = df_feature_importances[['index', 'importance_%']].head(top_n)

    row_height = 0.5
    fig_height = len(df_display) * row_height + 2

    fig, ax = plt.subplots(figsize=(8, fig_height))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')

    table = ax.table(
        cellText  = df_display.values,
        colLabels = df_display.columns,
        cellLoc   = 'center',
        loc       = 'center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df_display.columns))))

    for (row, col), cell in table.get_celld().items():
        cell.set_facecolor('white')
        cell.set_edgecolor('black')
        cell.set_text_props(color='black')
        cell.set_height(1.0 / (len(df_display) + 1))  # 셀 높이 균등 분배

    plt.title(f'Feature Importances (Top {top_n})', fontsize=13, color='black', pad=10)
    plt.tight_layout()
    plt.show(block=True)

    return df_feature_importances