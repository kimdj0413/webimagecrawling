import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime, timedelta

"""
df = pd.read_csv('all.csv')

# ##    정렬
# df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m%d')
# df = df.sort_values(by=['code','날짜','시간'])
# df = df.reset_index(drop=True)
# df = df.iloc[:,1:]

# ##    난수 처리
# df = df.dropna(subset=['MA120'])

# df.to_csv('all.csv')

print(df.head())

##      거래량 스케일링
financeList = pd.read_csv('FinanceListPreprocess.csv')
name = financeList['종목코드'].tolist()
volSum = financeList['상장주식수'].tolist()
finance_dict = dict(zip(name, volSum))
df = df.iloc[:, 1:]
df['code'] = df['code'].astype(str).str.zfill(6)

def divide_volumes(row):
    try:
        divisor = finance_dict[row['code']]
        row[['거래량', '매도량', '매수량']] = row[['거래량', '매도량', '매수량']]*1000000 / divisor
        row['거래량'] = round(row['거래량'], 2)
        row['매도량'] = round(row['매도량'], 2)
        row['매수량'] = round(row['매수량'], 2)
    except KeyError:
        print(f"코드 {row['code']}를 찾지 못했습니다.")
        input()
    return row

output_file = 'allTemp.csv'
df.head(0).to_csv(output_file, index=False)
cnt = 0

for idx, row in df.iterrows():
    processed_row = divide_volumes(row)
    processed_row.to_frame().T.to_csv(output_file, index=False, mode='a', header=False)
    if cnt % 1000 == 0:
        print(f'{cnt}개 처리 완료')
    cnt += 1

print("데이터 처리 완료")
"""
# 데이터 로드
df = pd.read_csv('allTemp.csv')

# Unique 코드 및 카운트 계산
counts = df['code'].value_counts()
counts_dict = counts.to_dict()

# 결과를 저장할 리스트
results = []

for key in tqdm(counts_dict.keys()):
    value = counts_dict[key]
    for i in range(value - 9):   # 예측 분 -1
        start_idx = counts_dict[key] - value + i
        end_idx = start_idx + 4  # 묶을 분 -1

        # 벡터화하여 연산
        vectorList = []
        for col in ['시가', '고가', '저가', '종가', '거래량', '매도량', '매수량', 'MA5', 'MA20', 'MA60', 'MA120', 'Upper_Band', 'Lower_Band']:
            diff = df[col].values[start_idx:end_idx] - df[col].values[start_idx + 1:end_idx + 1]
            vectorList.extend(round(d, 2) for d in diff)

        openValue = df['시가'][start_idx + 9] - df['시가'][start_idx]
        if openValue > 0:
            vectorList.append(2.0)
        elif openValue == 0:
            vectorList.append(1.0)
        else:
            vectorList.append(0.0)

        results.append(vectorList)

# 결과를 DataFrame으로 변환
results_df = pd.DataFrame(results)

# CSV 파일에 저장
results_df.to_csv('allVector.csv', index=False)
'''
##      난수 및 의미 없는 데이터 삭제
df = pd.read_csv('allVector.csv')
df.columns = [f"Column{i+1}" for i in range(df.shape[1])]
mask = (df.iloc[:, :-1] == 0.0).all(axis=1)
num_zero_rows = mask.sum()
print(f"마지막 열의 값을 제외하고 다른 값들이 모두 0.0인 행의 갯수: {num_zero_rows}")
df = df[~mask]
df = df.dropna()

##    라벨 비율 맞추기
value_counts = df['Column53'].value_counts()
print("각 값의 갯수:")
print(value_counts)

min_count = value_counts.min()
balanced_df_list = []
for value in value_counts.index:
    subset = df[df['Column53'] == value].sample(n=min_count, random_state=42)
    balanced_df_list.append(subset)
df = pd.concat(balanced_df_list).reset_index(drop=True)
print(len(df))
df.to_csv('readyAll1.csv')
'''