import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime, timedelta

df = pd.read_csv('all.csv')
"""
# ##    정렬
# df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m%d')
# df = df.sort_values(by=['code','날짜','시간'])
# df = df.reset_index(drop=True)
# df = df.iloc[:,1:]

# ##    난수 처리
# df = df.dropna(subset=['MA120'])

# df.to_csv('all.csv')

print(df.head())
"""
# 데이터 로드
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

# 새로운 CSV 파일에 첫 번째 줄을 헤더와 함께 저장
output_file = 'allTemp.csv'
df.head(0).to_csv(output_file, index=False)
cnt = 0
# 한 줄씩 처리하여 저장
for idx, row in df.iterrows():
    processed_row = divide_volumes(row)
    processed_row.to_frame().T.to_csv(output_file, index=False, mode='a', header=False)
    if cnt % 1000 == 0:
        print(f'{cnt}개 처리 완료')
    cnt += 1

print("데이터 처리가 완료되었습니다.")
"""
uniqueElement = df['code'].unique()
counts = df['code'].value_counts()
counts_dict = counts.to_dict()

startIndex = 0
first_write = True

for key in tqdm(uniqueElement):
    value = counts_dict.get(key, 0)
    for i in range(startIndex, startIndex+value-9):   # 예측 분 -1 ex) 10분 예측 startIndex+value-9
        vectorList = []
        for j in range(i, i+4):   # 묶을 분 -1 ex) 5분 묶기 i+4
            vectorList.append(round(df['시가'][j]-df['시가'][j+1],2))
            vectorList.append(round(df['고가'][j]-df['고가'][j+1],2))
            vectorList.append(round(df['저가'][j]-df['저가'][j+1],2))
            vectorList.append(round(df['종가'][j]-df['종가'][j+1],2))
            vectorList.append(round(df['거래량'][j]-df['거래량'][j+1],2))
            vectorList.append(round(df['매도량'][j]-df['매도량'][j+1],2))
            vectorList.append(round(df['매수량'][j]-df['매수량'][j+1],2))
            vectorList.append(round(df['MA5'][j]-df['MA5'][j+1],2))
            vectorList.append(round(df['MA20'][j]-df['MA20'][j+1],2))
            vectorList.append(round(df['MA60'][j]-df['MA60'][j+1],2))
            vectorList.append(round(df['MA120'][j]-df['MA120'][j+1],2))
            vectorList.append(round(df['Upper_Band'][j]-df['Upper_Band'][j+1],2))
            vectorList.append(round(df['Lower_Band'][j]-df['Lower_Band'][j+1],2))

        openValue = df['시가'][i+9]-df['시가'][i]
        openValuePercent = openValue/df['시가'][i]*100

        if openValuePercent >= 1:
            vectorList.append(3.0)
        elif openValuePercent >= 0 and openValuePercent < 1:
            vectorList.append(2.0)
        elif openValuePercent < 0 and openValuePercent > -1:
            vectorList.append(1.0)
        else:
            vectorList.append(0.0)

        # 데이터프레임으로 변환
        temp_df = pd.DataFrame([vectorList])

        # CSV 파일에 추가
        temp_df.to_csv('allVector.csv', mode='a', header=first_write, index=False)
        first_write = False

    startIndex += value

##      난수 및 의미 없는 데이터 삭제
df = pd.read_csv('allVector.csv')
df.columns = [f"Column{i+1}" for i in range(df.shape[1])]
mask = (df.iloc[:, :-1] == 0.0).all(axis=1)
num_zero_rows = mask.sum()
print(f"마지막 열의 값을 제외하고 다른 값들이 모두 0.0인 행의 갯수: {num_zero_rows}")
df = df[~mask]
df = df.dropna()

##    라벨 비율 맞추기
value_counts = df['Column49'].value_counts()
print("각 값의 갯수:")
print(value_counts)

min_count = value_counts.min()
balanced_df_list = []
for value in value_counts.index:
    subset = df[df['Column49'] == value].sample(n=min_count, random_state=42)
    balanced_df_list.append(subset)
df = pd.concat(balanced_df_list).reset_index(drop=True)
print(len(df))

df = df.iloc[:,1:]
df.to_csv('ready4.csv')
"""