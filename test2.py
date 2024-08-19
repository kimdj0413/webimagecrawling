import pandas as pd
import numpy as np
from tqdm import tqdm

# 데이터 로드
df = pd.read_csv('allMillion.csv')

# 필요한 열 선택 및 계산
# '시가'와 '종가' 열의 차이를 계산하여 새로운 열에 저장
df['price_diff'] = (df['시가'].shift(-9) - df['시가'].shift(-2)) / df['시가'].shift(-2) * 100

# 각 조건에 따라 카운트를 위한 배열 초기화
dataA = np.sum(df['price_diff'] >= 0)
dataB = np.sum(df['price_diff'] < -0)

# 총합 계산
sumData = dataA + dataB

# 결과 출력
if sumData > 0:
    print(f'A : {round(dataA / sumData * 100,2)}%, B : {round(dataB / sumData * 100,2)}%')
else:
    print("No data to process.")