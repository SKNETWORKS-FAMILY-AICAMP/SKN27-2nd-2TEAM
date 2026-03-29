'''
'''
# 라이브러리, 의존성 선언 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, r2_score, confusion_matrix, classification_report

# 실행 함수 
def simul_netflex():

    # 1. 데이터 로드 #########################################################################################

    # CSV 파일을 로드하여 데이터프레임에 주입
    # 폴더 구조 다르니까 파일 경로 수정해야 함 
    df = pd.read_csv('models/data/netflix_user_behavior_dataset.csv')

    # 로드한 데이터 확인
    print(f'{df.shape}')
    print(f'{df.columns}')
    print(f'{df.head(1)}')

    # 로드한 데이터에서 결측치 있는지 체크
    # 문제되는 데이터 있는지 확인
    # 데이터 분석 진행 

    # 2. 분리 전 사전 준비 #########################################################################################

    # 타겟 데이터가 churned 인데 Yes / No 로 되어 있음 > 1, 0으로 변경해야 함 
    df['churned'] = df['churned'].map({'Yes': 1, 'No': 0})

    # 3. 데이터 분리 #########################################################################################

    # feature와 target 데이터로 나눔
    X = df.drop('churned',axis=1)
    y = df['churned']

    # train 과 test 데이터로 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42) 

    print(f'{X_train.shape}, {X_test.shape}, {y_train.shape}, {y_test.shape}')


    # 4. 데이터 전처리 #########################################################################################

    train = X_train.copy()
    test = X_test.copy()

    # 컬럼 제거 (사용하지 않을 컬럼 drop)
    # 1) 제거할 컬럼 리스트 정리
    drop_columns = df.select_dtypes(exclude=np.number).columns
    # 2) 컬럼 제거
    train = train.drop(drop_columns, axis=1)
    test = test.drop(drop_columns, axis=1)

    # 3) 컬럼 제거 후 남은 컬럼 확인
    print(f'{train.info()}')
    print(f'{test.info()}')

    # 결측치 제거
    # 중복값 제거
    # 인코딩 (숫자 아닌 컬럼 -> 숫자로 변경)

    # 5. 모델 학습 (train 데이터 fit) #########################################################################################

    # 저장했던 모델 로드 (모델 학습 시에는 모델 선언 / 학습 하는 과정이 있었음 )

    model = joblib.load('models/model_netflex.pkl')


    # 6. 모델 예측 (test 데이터 pred) #########################################################################################
    
    # 모델 예측 결과 확인
    y_true = y_test
    y_pred = model.predict(test) # 모델 예측 // test == 처리 후 X_test 

    print(f'{y_pred.shape}')
    print(f'{y_pred}')


    # 7. 모델/결과 저장 #########################################################################################

    # 저장한 모델을 사용하는거니 다시 저장안함 
    
    # 8. 결과 표시 / 시각화 #########################################################################################

    # 정확도 확인 
    accuracy = accuracy_score(y_true=y_true, y_pred=y_pred)
    print(f'\n 정확도: {accuracy} \n')

    # confusion matrix 
    print(f'\n===confusion matrix===\n')
    cm = confusion_matrix(y_true, y_pred)
    print(cm)

    tn, fp, fn, tp = cm.ravel()
    print(f'tn:{tn}')
    print(f'fp:{fp}')
    print(f'fn:{fn}')
    print(f'tp:{tp}')

    print(f'\n===Classification Report===\n')
    print(classification_report(y_true, y_pred))

    # confusion matrix 시각화
    plt.figure(figsize=(8,6)) # 그래프 영역
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Pred_label')
    plt.ylabel('True_label')
    plt.title('confusion matrix')
    plt.show()

    # feature 중요도 확인 
    feature_importance = pd.DataFrame({
        'feature': train.columns,
        'importance': model.feature_importances_,
    }).sort_values('importance', ascending=False)

    print('\n===상위 feature 10개===\n')
    print(feature_importance.head(10))


if __name__ == '__main__':
    simul_netflex()
