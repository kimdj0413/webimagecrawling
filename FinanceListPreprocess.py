import pandas as pd
import numpy as np

df = pd.read_csv('minuteFinance.csv')
"""
print(df[:3])
newDf = df[['종목코드','종목명','상장주식수']]
print(newDf[:3])
newDf.to_csv('FinanceListPreprocess.csv')
print(len(newDf)-1)
"""

# df = df.iloc[1717:]
# df.to_csv('minuteFinance.csv')
# print(df)

##    이상한 주식 지우기
# num = ''
# df = df[~df['Finance'].str.contains(num)]
# df.to_csv('minuteFinance.csv', index=True)

#    중첩 저장 처리
uniqueElement = df['Finance'].unique()
counts = df['Finance'].value_counts()
print(counts[30:50])

# df = pd.read_csv('FinanceList.csv', encoding='cp949')
# df.to_csv('FinanceList.csv', encoding='utf8')
# print(df)