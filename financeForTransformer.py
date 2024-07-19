import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('ready.csv')
df = df.iloc[:,1:]
df['label'] = df.iloc[:,-1:]

df['combined'] = df.iloc[:, :-1].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
df_result = df[['combined', 'label']]
"""
df_result.to_csv('ready1.csv')

df = pd.read_csv('ready1.csv')
df = df.iloc[:,2:]
df.to_csv('ready1.csv',index=False)
"""
df_result = df_result[df_result['combined'].apply(len) <= 300]
lengths = df_result['combined'].apply(len)
df_result.to_csv('ready1.csv',index=False)
max_length = lengths.max()
min_length = lengths.min()
mean_length = lengths.mean()

print(f"최댓값: {max_length}")
print(f"최솟값: {min_length}")
print(f"평균값: {mean_length:.2f}")

plt.figure(figsize=(12, 6))
plt.hist(lengths, bins=range(min(lengths), max(lengths) + 2), edgecolor='black', alpha=0.7)
plt.title('첫 번째 열의 문자열 길이 분포')
plt.xlabel('문자열 길이')
plt.ylabel('빈도')
plt.xticks(range(min(lengths), max(lengths) + 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()
