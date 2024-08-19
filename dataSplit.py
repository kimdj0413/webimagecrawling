import pandas as pd
import numpy as np

df = pd.read_csv('allReady1.csv')
# col45의 고유값과 개수 파악
value_counts = df['col45'].value_counts()

# 가장 적은 개수를 가진 고유값의 개수
min_count = value_counts.min()

# 샘플링 결과 저장을 위한 리스트
samples = []

# 각 고유값에 대해 샘플링 (무작위로 섞어서)
for value in value_counts.index:
    # 각 고유값의 데이터 섞기
    shuffled_data = df[df['col45'] == value].sample(frac=1, random_state=1)
    # 섞인 데이터에서 min_count 만큼 샘플링
    sampled = shuffled_data.head(min(min_count, len(shuffled_data)))
    samples.append(sampled)

# 최종 샘플 데이터프레임 생성
result_df = pd.concat(samples).reset_index(drop=True)

# 최종 결과 무작위로 섞기 (선택적)
result_df = result_df.sample(frac=1, random_state=1).reset_index(drop=True)
result_df.to_csv('./split/split.csv')
"""
# col45의 고유 값에 따라 그룹화
grouped = df.groupby('col45')

# 각 그룹에서 균등하게 샘플링
samples = grouped.apply(lambda x: x.sample(n=len(x), random_state=1)).reset_index(drop=True)

# 샘플을 섞기
samples = samples.sample(frac=1, random_state=1).reset_index(drop=True)

# 최종 샘플을 6개로 나누기
num_splits = 1
split_size = len(samples) // num_splits
splits = [samples.iloc[i * split_size:(i + 1) * split_size] for i in range(num_splits)]

# 마지막 분할이 남은 경우 처리
if len(samples) % num_splits != 0:
    splits[-1] = pd.concat([splits[-1], samples.iloc[num_splits * split_size:]])

# 결과를 CSV로 저장
for i, split in enumerate(splits):
    split.to_csv(f'./split/split_{i + 1}.csv', index=False)

print("CSV 파일로 저장 완료.")
"""