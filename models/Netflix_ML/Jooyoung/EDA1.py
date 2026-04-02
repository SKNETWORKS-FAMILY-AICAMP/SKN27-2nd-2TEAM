import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# 한글 깨짐 방지 (필요 시 주석 해제)
# plt.rcParams['font.family'] = 'Malgun Gothic' 
# plt.rcParams['axes.unicode_minus'] = False

# file_path = r'C:\dev\project\SKN27-2nd-2TEAM\models\Netflix_ML\Jooyoung'
# file_name = 'refined_netflix_data.csv'


file_path = r'C:\dev\project\SKN27-2nd-2TEAM\models\Netflix_ML\JAEKANG'
file_name = 'new_user_with_features.csv'



# 데이터 로드
df = pd.read_csv(os.path.join(file_path, file_name))

# 1. 수치형 데이터 간의 상관관계 히트맵
# [수정] numeric_only=True를 추가하여 문자열 컬럼 제외 오류 방지
plt.figure(figsize=(10, 8))
numeric_df = df.select_dtypes(include=[np.number]) # 수치형 데이터만 명시적으로 선택
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Feature Correlation Heatmap")
plt.tight_layout() # 그래프 잘림 방지
plt.show()

# 2. 구독 플랜별 완독률 분포 (Boxplot)
plt.figure(figsize=(8, 6))
sns.boxplot(x='subscription_type', y='completion_rate', data=df, 
            order=['Basic', 'Standard', 'Premium', 'Premium+']) 
plt.title("Completion Rate by Subscription Type")
plt.show()

# 3. 나이와 시간당 비용의 관계 (Scatter plot)
# [수정] cost_per_hour 계산 시 발생했을 수 있는 Inf(무한대)나 NaN 값 제거 후 시각화
plot_data = df.replace([np.inf, -np.inf], np.nan).dropna(subset=['age', 'cost_per_hour'])
sns.jointplot(x='age', y='cost_per_hour', data=plot_data, kind='reg', color='teal')
plt.show()