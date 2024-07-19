import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from tqdm import tqdm
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.manifold import MDS


print(df[:3])
newDf = df[['종목코드','종목명','상장주식수']]
print(newDf[:3])
newDf.to_csv('FinanceListPreprocess.csv')
print(len(newDf)-1)


# df = df.iloc[1717:]
# df.to_csv('minuteFinance.csv')
# print(df)

##    이상한 주식 지우기
# num = ''
# df = df[~df['Finance'].str.contains(num)]
# df.to_csv('minuteFinance.csv', index=True)

#    중첩 저장 처리
# uniqueElement = df['Finance'].unique()
# counts = df['Finance'].value_counts()
# print(len(df))
# print(len(uniqueElement))
# filtered_df = df[df['Finance'].isin(counts[counts >= 1000].index)]
# print(len(filtered_df))
# uniqueElement = filtered_df['Finance'].unique()
# counts = filtered_df['Finance'].value_counts()
# print(len(uniqueElement))
# filtered_df.to_csv('minuteFinance.csv')

# plt.figure(figsize=(10, 6))
# counts.plot(kind='bar')
# plt.title('Distribution of Finance Values')
# plt.xlabel('Finance Value')
# plt.ylabel('Count')
# plt.xticks(rotation=45)
# plt.show()

# df = pd.read_csv('FinanceList.csv', encoding='cp949')
# df.to_csv('FinanceList.csv', encoding='utf8')
# print(df)

##    빈 시간 추가하기
df = pd.read_csv('minuteFinance.csv')
uniqueElement = df['Finance'].unique()
counts = df['Finance'].value_counts()
counts_dict = counts.to_dict()

startIndex = 0
for key in tqdm(uniqueElement):
  value = counts_dict.get(key, 0)
  preDate = datetime.strptime(df['Datetime'][startIndex],'%Y-%m-%d %H:%M')
  for i in range(startIndex, startIndex+value):
    nowDate = datetime.strptime(df['Datetime'][i],'%Y-%m-%d %H:%M')
    if preDate == nowDate:
      # print(f'[{nowFinance}] Correct! predate : {preDate}, nowdate : {nowDate}')
      preDate += timedelta(minutes=1)
    else:
      onlyPreDate = preDate.strftime('%Y-%m-%d')
      onlyNowDate = nowDate.strftime('%Y-%m-%d')
      # print(f'onlypredate : {onlyPreDate}, onlynowdate : {onlyNowDate}')
      if onlyNowDate == onlyPreDate:
        while(True):
          # print(f'[{nowFinance}]Wrong! predate : {preDate}, nowdate : {nowDate}')
          dateCut = preDate.strftime('%Y-%m-%d %H:%M')
          newRow = {'Unnamed: 0':len(df),'Datetime':dateCut,'Day':df['Day'][i-1],'Finance':df['Finance'][i-1],'Open':df['Open'][i-1],'High':df['High'][i-1],'Low':df['Low'][i-1],'Close':df['Close'][i-1],'Adj Close':df['Adj Close'][i-1],'Volume':0,'MA5':df['MA5'][i-1],'MA20':df['MA20'][i-1],'MA60':df['MA60'][i-1],'Rolling_Mean':df['Rolling_Mean'][i-1],'Upper_Band':df['Upper_Band'][i-1],'Lower_Band':df['Lower_Band'][i-1]}
          df.loc[len(df)] = newRow
          preDate += timedelta(minutes=1)
          if(preDate == nowDate):
            # print(f'[{nowFinance}] Correct! predate : {preDate}, nowdate : {nowDate}')
            preDate += timedelta(minutes=1)
            break
      else:
        preDate = nowDate
  # print(df)
  # input()
  startIndex += value

df.to_csv('MinuteCandle.csv')


df = pd.read_csv("MinuteCandle.csv")
##    정렬, 쓸데없는 열 제거, 요일을 숫자로
df['Datetime'] = pd.to_datetime(df['Datetime'])
df = df.sort_values(by=['Finance', 'Datetime'])
df = df.iloc[:, 2:]
df = df.reset_index(drop=True)

df.to_csv('readytovector.csv')

# day_to_number = {
#     'Mon': 1,
#     'Tue': 2,
#     'Wed': 3,
#     'Thu': 4,
#     'Fri': 5,
#     'Sat': 6,
#     'Sun': 7
# }
# df['Day'] = df['Day'].map(day_to_number)


##    벡터 생성
df = pd.read_csv('readytovector.csv')

uniqueElement = df['Finance'].unique()
counts = df['Finance'].value_counts()
counts_dict = counts.to_dict()

startIndex = 0
data = []
for key in tqdm(uniqueElement):
  value = counts_dict.get(key, 0)
  vectorList = []
  for i in range(startIndex, startIndex+value-9):   # 예측 분 -1 ex) 10분 예측 startIndex+value-9
    vectorList = []
    for j in range(i, i+4):   # 묶을 분 -1 ex) 5분 묶기 i+4
      vectorList.append(round(df['Open'][j]-df['Open'][j+1],2))
      vectorList.append(round(df['High'][j]-df['High'][j+1],2))
      vectorList.append(round(df['Low'][j]-df['Low'][j+1],2))
      vectorList.append(round(df['Close'][j]-df['Close'][j+1],2))
      vectorList.append(round(df['Adj Close'][j]-df['Adj Close'][j+1],2))
      vectorList.append(round(df['Volume'][j]-df['Volume'][j+1],2))
      vectorList.append(round(df['MA5'][j]-df['MA5'][j+1],2))
      vectorList.append(round(df['MA20'][j]-df['MA20'][j+1],2))
      vectorList.append(round(df['MA60'][j]-df['MA60'][j+1],2))
      vectorList.append(round(df['Rolling_Mean'][j]-df['Rolling_Mean'][j+1],2))
      vectorList.append(round(df['Upper_Band'][j]-df['Upper_Band'][j+1],2))
      vectorList.append(round(df['Lower_Band'][j]-df['Lower_Band'][j+1],2))
    
    # 다음 Open만 포함
    # vectorList.append(round(df['Open'][i+4],2))
    openValue = df['Open'][i+9]-df['Open'][i]
    openValuePercent = openValue/df['Open'][i]*100
    
    if openValuePercent >= 1:
      vectorList.append(3.0)
    elif openValuePercent >= 0 and openValuePercent < 1:
      vectorList.append(2.0)
    elif openValuePercent < 0 and openValuePercent > -1:
      vectorList.append(1.0)
    else:
      vectorList.append(0.0)
    
    data.append(vectorList)
  startIndex += value
df = pd.DataFrame(data)
df.to_csv('FinanceVector.csv', index=False)

##    값이 모두 0.0인 행 삭제, 난수 행 삭제, 라벨 비율 맞추기
df = pd.read_csv('FinanceVector.csv')
df.columns = [f"Column{i+1}" for i in range(df.shape[1])]
print(df[:3])

mask = (df.iloc[:, :-1] == 0.0).all(axis=1)
num_zero_rows = mask.sum()
print(f"마지막 열의 값을 제외하고 다른 값들이 모두 0.0인 행의 갯수: {num_zero_rows}")
df = df[~mask]
df = df.dropna()
# df = df.iloc[:,2:]
df.to_csv('readytemp.csv')

##    라벨 비율
df = pd.read_csv('readytemp.csv')
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

##    PCA 주성분 분석
df = pd.read_csv('ready.csv')
df_except_last = df.iloc[:, 1:-1]
pca = PCA(n_components=1)

pca_columns = []
for i in range(0, len(df_except_last.columns), 12):
    subset = df_except_last.iloc[:, i:i+12]
    pca_result = pca.fit_transform(subset)
    pca_columns.append(pca_result)
pca_df = pd.DataFrame(np.hstack(pca_columns), columns=[f'PCA_{i//12+1}' for i in range(0, len(df_except_last.columns), 12)])
pca_df['Column49'] = df.iloc[:, -1].values

pca_df.to_csv('pca.csv',index=False)
