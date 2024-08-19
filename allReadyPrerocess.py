import numpy as np
import pandas as pd
import os
from tqdm import tqdm
import pandas as pd
import numpy as np

df = pd.read_csv('allMillionVector.csv')
# col45의 고유 값에 따라 그룹화 후 균등하게 샘플링
grouped = df.groupby('col45')

# 각 그룹에서 균등하게 샘플링할 수 있는 수 계산
min_size = grouped.size().min()  # 가장 작은 그룹의 크기

# 각 그룹에서 샘플링
samples = grouped.apply(lambda x: x.sample(n=min_size, random_state=1)).reset_index(drop=True)

# 샘플을 섞기
samples = samples.sample(frac=1, random_state=1).reset_index(drop=True)

# 최종 샘플을 6개로 나누기
split_size = len(samples) // 4
splits = [samples.iloc[i * split_size:(i + 1) * split_size] for i in range(4)]

# 마지막 분할이 남은 경우 처리
if len(samples) % 4 != 0:
    splits[-1] = pd.concat([splits[-1], samples.iloc[4 * split_size:]])

# 결과를 CSV로 저장
for i, split in enumerate(splits):
    split.to_csv(f'./split/split_{i + 1}.csv', index=False)

print("CSV 파일로 저장 완료.")

"""
df = pd.read_csv('allMillionVector.csv')
print(len(df))
df = df[~df.isin([999999, 99]).any(axis=1)]
df_cleaned = df[~(df.iloc[:, :-1].sum(axis=1) == 0)]
df = df[np.isfinite(df).all(axis=1)]
df = df.dropna()

def remove_outliers_iqr(df):
    for column in df.columns:
        Q1 = df[column].quantile(0.01)  # 1사분위수
        Q3 = df[column].quantile(0.99)  # 3사분위수
        IQR = Q3 - Q1  # IQR 계산

        # 아웃라이어의 경계 설정
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # 아웃라이어 제거
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    return df

# 아웃라이어 제거
df = remove_outliers_iqr(df)
unique_values = df['col45'].unique()
df.to_csv('allReady1.csv')
print(len(df))
"""
df = pd.read_csv('./split/split_20.csv')
print(df.info())
value_counts = df['col45'].value_counts(normalize=True)
print("col45의 고유 값 비율:\n", value_counts)
