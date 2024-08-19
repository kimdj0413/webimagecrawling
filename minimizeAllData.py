import numpy as np
import pandas as pd
import os
from tqdm import tqdm
"""
##    700000 줄로 자르기, 쓸데없는 열 지우기
df = pd.read_csv('all.csv',encoding='cp949')
df = df.drop(columns=['day_name','매도량','매수량'])
df['거래평균'] = round(df['거래량'].rolling(window=14).mean(),2)
df = df.iloc[:,1:]
df.to_csv('allMillion.csv',index=False)

##    난수 날리기
df = pd.read_csv('allMillion.csv')
df = df.dropna()
df = df.reset_index(drop=True)
df.to_csv('allMillion.csv')
"""
# CSV 파일 읽기 및 전처리
df = pd.read_csv('allMillion.csv')
df = df.iloc[:, 3:]
df = df.astype('float32')
print(df)
print(df.info())

uniqueCnt = df['code'].value_counts()
uniqueDict = uniqueCnt.to_dict()

# 벡터 만들기
def generate_column_names(num_columns):
    return [f'col{i+1}' for i in range(num_columns)]

# 청크 크기 설정
chunk_size = 10000
all_vectors = []

index = 0
columns = ['시가', '고가', '저가', '종가', 'MA5', 'MA20', 'MA60', 'MA120', 'Upper_Band', 'Lower_Band']

for key in tqdm(uniqueDict):
    indices = df[df['code'] == key].index.to_numpy()
    num_records = len(indices)

    # 8분 예측을 위한 인덱스 범위 설정
    for i in tqdm(range(num_records - 9)):
        vectorList = []

        # 5분 묶기 계산
        for j in range(4):
            current_index = indices[i + j]
            next_index = indices[i + j + 1]

            for column in columns:
                if df.at[current_index, column] != 0:
                    value_change = (df.at[next_index, column] - df.at[current_index, column]) / df.at[current_index, column] * 100
                    vectorList.append(value_change)
                else:
                    vectorList.append(999999)

            if df.at[current_index, '거래평균'] != 0:
                volume_change = (df.at[next_index, '거래량'] - df.at[current_index, '거래량']) / df.at[current_index, '거래평균'] * 100
                vectorList.append(volume_change)
            else:
                vectorList.append(999999)

        # 종가 예측
        if df.at[indices[i + 4], '종가'] != 0:
            resultValue = (df.at[indices[i + 9], '시가'] - df.at[indices[i], '시가']) / df.at[indices[i], '시가'] * 100
            vectorList.append(1 if resultValue >= 0 else 0)
        else:
            vectorList.append(99)

        # 벡터를 리스트에 추가
        all_vectors.append(vectorList)
        
        # 청크 크기에 도달하면 CSV에 저장
        if len(all_vectors) >= chunk_size:
            result_df = pd.DataFrame(all_vectors, columns=generate_column_names(len(all_vectors[0])))
            result_df.to_csv('D:/Data/allMillionVector.csv', mode='a', header=not os.path.exists('allMillionVector.csv'), index=False)
            all_vectors = []  # 리스트 초기화
    
    index += uniqueDict[key]

# 남아있는 벡터를 저장
if all_vectors:
    result_df = pd.DataFrame(all_vectors, columns=generate_column_names(len(all_vectors[0])))
    result_df.to_csv('D:/Data/allMillionVector.csv', mode='a', header=not os.path.exists('allMillionVector.csv'), index=False)
##      999999가 포함된 열 지우기 & 라벨이 99인거 지우기
"""
df = pd.read_csv('allMillionVector.csv', on_bad_lines='skip')
# df = df.astype('float16')
print(len(df))
print(df.info())
print(df.head())
# 모든 열에 대해 숫자로 변환 시도
df = df.apply(pd.to_numeric, errors='coerce')
# NaN 값이 있는 행 삭제
df = df.dropna()
df = df.astype('float16')
df.to_csv('allReady1.csv')
print(len(df))
print(df.info())
print(df.head())
"""