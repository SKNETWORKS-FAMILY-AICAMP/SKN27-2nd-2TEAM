import os
import numpy as np
import random
import torch

def reset_seeds(seed=42):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)    # 파이썬 환경변수 시드 고정
    np.random.seed(seed)
    torch.manual_seed(seed) # cpu 연산 무작위 고정
    torch.cuda.manual_seed(seed) # gpu 연산 무작위 고정
    torch.backends.cudnn.deterministic = True  # cuda 라이브러리에서 Deterministic(결정론적)으로 예측하기 (예측에 대한 불확실성 제거 )


def get_null_info(train, test):
  
  lst_null = []
  for dataset in [train, test]:
    dataset_null = train_null_info = (train.isnull().sum() / len(train)).round(4).sort_values(ascending=False)
    lst_null.append(dataset_null)

  return lst_null
def get_null_cols(train, test):
    lst_null = get_null_info(train, test)

    return {
      "train": lst_null[0][lst_null[0] > 0].index,
      "test": lst_null[1][lst_null[1] > 0].index
    }

