import yfinance as yf
import datetime

# 삼성전자 티커
ticker = '000660.KS'

# 데이터 가져올 기간 설정 (예: 최근 7일)
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=7)

# 삼성전자 분봉 데이터 다운로드
data = yf.download(ticker, start=start_date, end=end_date, interval='1m')

# 데이터 출력
print(data)