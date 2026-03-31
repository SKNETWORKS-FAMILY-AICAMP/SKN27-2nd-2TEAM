import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ─────────────────────────────────────────
# 1. IQR 기반 이상치 탐지 요약
# ─────────────────────────────────────────
def detect_outliers(train: pd.DataFrame) -> pd.DataFrame:
    """IQR 기반 이상치 탐지 결과 출력 및 요약 DataFrame 반환"""

    num_cols = train.select_dtypes(include=['number']).columns

    print("=" * 55)
    print("        IQR 기반 이상치 탐지 결과 (train 기준)")
    print("=" * 55)

    outlier_summary = []

    for col in num_cols:
        Q1  = train[col].quantile(0.25)
        Q3  = train[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outlier_mask  = (train[col] < lower) | (train[col] > upper)
        outlier_count = outlier_mask.sum()
        outlier_ratio = outlier_count / len(train) * 100

        outlier_summary.append({
            'column'       : col,
            'Q1'           : round(Q1, 2),
            'Q3'           : round(Q3, 2),
            'IQR'          : round(IQR, 2),
            'lower_bound'  : round(lower, 2),
            'upper_bound'  : round(upper, 2),
            'outlier_count': outlier_count,
            'outlier_ratio': f'{outlier_ratio:.2f}%'
        })

        print(f"\n [{col}]")
        print(f"   정상 범위 : {round(lower, 2)} ~ {round(upper, 2)}")
        print(f"   이상치 수 : {outlier_count}개 ({outlier_ratio:.2f}%)")

    print("\n" + "=" * 55)

    return pd.DataFrame(outlier_summary)


# ─────────────────────────────────────────
# 2. IQR 기반 이상치 시각화
# ─────────────────────────────────────────
def plot_outliers(train: pd.DataFrame) -> None:
    """IQR 기반 이상치 박스플롯 시각화"""

    num_cols = train.select_dtypes(include=['number']).columns

    fig, axes = plt.subplots(1, len(num_cols), figsize=(5 * len(num_cols), 5))
    if len(num_cols) == 1:
        axes = [axes]

    for ax, col in zip(axes, num_cols):
        Q1  = train[col].quantile(0.25)
        Q3  = train[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        sns.boxplot(y=train[col], ax=ax, color='skyblue')
        ax.axhline(lower, color='red', linestyle='--', linewidth=1, label=f'lower: {lower:.1f}')
        ax.axhline(upper, color='red', linestyle='--', linewidth=1, label=f'upper: {upper:.1f}')
        ax.set_title(col)
        ax.legend(fontsize=8)

    plt.suptitle('IQR 기반 이상치 탐지', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()