import pandas as pd

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    전처리 로직을 담은 함수 (ML 파트 제공 예정)
    학습 시 사용한 로직과 동일하게 적용해야 하며,
    현재는 뼈대 구조로 데이터프레임을 그대로 반환합니다.
    """
    # 결측치 처리, 인코딩, 스케일링 등 작성
    return df