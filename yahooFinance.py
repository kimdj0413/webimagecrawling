import yfinance as yf
import datetime
import pandas as pd
import csv

##    주식 데이터 가져오기
financeList = pd.read_csv('FinanceListPreprocess.csv')
name = financeList['종목코드'].tolist()
volSum = financeList['상장주식수'].tolist()

class YFTzMissingError(Exception):
    pass

for i in range(len(name)):
  try:
    print(name[i], volSum[i])
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=7)
    df = yf.download(name[i] + '.KS', start=start_date, end=end_date, interval='1m')
    
    ##    종목 번호 넣기
    df['Finance'] = name[i]
    columns = df.columns.tolist()
    new_order = columns[:0] + ['Finance'] + columns[0:-1]
    df = df[new_order]

    ##    날짜 형식 맞추기 및 요일 추가 하기
    df.index = df.index.strftime('%Y-%m-%d %H:%M')
    df.insert(0, 'Day', pd.to_datetime(df.index).strftime('%a'))

    ##    상장 주식수 정규화
    df['Volume'] = round(df['Volume']*1000000 / volSum[i], 3)

    ##    이평선 추가
    df['MA5'] = round(df['Close'].rolling(window=5).mean(),2)
    df['MA20'] = round(df['Close'].rolling(window=20).mean(),2)
    df['MA60'] = round(df['Close'].rolling(window=60).mean(),2)

    ##    볼린저밴드 추가하기
    def calculate_bollinger_bands(data, window, num_std):
        rolling_mean = data['Close'].rolling(window=window).mean()
        rolling_std = data['Close'].rolling(window=window).std()
        
        upper_band = rolling_mean + (rolling_std * num_std)
        lower_band = rolling_mean - (rolling_std * num_std)
        
        return rolling_mean, upper_band, lower_band
      
    window = 20
    num_std = 2
    rolling_mean, upper_band, lower_band = calculate_bollinger_bands(df, window, num_std)
    df['Rolling_Mean'] = round(rolling_mean,2)
    df['Upper_Band'] = round(upper_band,2)
    df['Lower_Band'] = round(lower_band,2)

    ##    null 처리 및 Volume = 0 처리
    df = df.dropna()
    df = df[df['Volume'] != 0]

    ##    저장
    preDf = pd.read_csv('minuteFinance.csv', index_col='Datetime')
    dfCombined = pd.concat([preDf, df])
    print(preDf[-10:])
    dfCombined.to_csv('minuteFinance.csv', index=True)
  except YFTzMissingError as e:
    ##    없는 주식 오류 처리
    print(f"{name[i]}주식 없음")
  except Exception as e:
    print("에러처리 완료")
  finally:
    continue

  # df.to_csv('minuteFinance.csv')
  # print(df)
  
  ## ~1718 지우기