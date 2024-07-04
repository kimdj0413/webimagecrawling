import yfinance as yf

financeName = '000660.KS'
ticker = yf.Ticker(financeName)
df = ticker.history(interval='5m', start='2023-07-02', end='2023-07-03', auto_adjust=False)

print(df)