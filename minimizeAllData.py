import numpy as np
import pandas as pd
import os
from tqdm import tqdm

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

##    각각 주식마다 갖고있는 열 개수 딕셔너리 만들기
df = pd.read_csv('allMillion.csv')
df = df.iloc[:,3:]
df = df.astype('float32')
print(df)
print(df.info())

uniqueCnt = df['code'].value_counts()
uniqueDict = uniqueCnt.to_dict()

##    벡터 만들기
#   컬럼명 생성
def generate_column_names(num_columns):
    return [f'col{i+1}' for i in range(num_columns)]

# 새로운 데이터 추가 함수
def append_to_csv(data):
    columns = generate_column_names(len(data))
    df_to_append = pd.DataFrame([data], columns=columns)
    df_to_append.to_csv('allMillionVector.csv', mode='a', header=not os.path.exists('allMillionVector.csv'), index=False)

index = 0
columns = ['시가', '고가', '저가', '종가', 'MA5', 'MA20', 'MA60', 'MA120', 'Upper_Band', 'Lower_Band']
for key in tqdm(uniqueDict):
  #   8분 예측
  for i in tqdm(range(index, index+uniqueDict[key]-7)):
    vectorList = []
    #   5분 묶기
    for j in range(0,4):
        for column in columns:
            if(df.iloc[i + j][column] != 0):
                vectorList.append((df.iloc[i + j + 1][column] - df.iloc[i + j][column]) / df.iloc[i + j][column]*100)
            else:
               vectorList.append(999999)
        if(df.iloc[i + j]['거래평균'] != 0):
            vectorList.append((df.iloc[i + j + 1]['거래량']-df.iloc[i + j]['거래량']) / df.iloc[i + j]['거래평균']*100)
        else:
           vectorList.append(999999)
    if(df.iloc[i+4]['종가'] != 0):
        resultValue = (df.iloc[i+7]['시가']-df.iloc[i+4]['종가']) / df.iloc[i+4]['종가'] * 100
        if resultValue >= 0.5:
            vectorList.append(3)
        elif resultValue >= 0 and resultValue < 0.5:
            vectorList.append(2)
        elif resultValue <= 0 and resultValue > -0.5:
            vectorList.append(1)
        else:
            vectorList.append(0)
    else:
       vectorList.append(99)
    append_to_csv(vectorList)
  index += uniqueDict[key]
##      999999가 포함된 열 지우기 & 라벨이 99인거 지우기
"""
##    데이터 타입 바꾸기(float16)
df = pd.read_csv('allMillionVector.csv')
df = df.astype('float16')
print(df)
print(df.info())


# df = pd.read_csv('allMillion.csv')
# df.to_csv('allMillion.csv',index=True)
# print(df)
"""