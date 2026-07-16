# pyrefly: ignore [missing-import]
import yfinance as yf
import datetime as dt

start_date = "2025-01-01"
end_date = dt.date.today()

companies = ["RELIANCE.NS", "IOC.NS", "BPCL.NS", "HINDPETRO.NS"]
df = yf.download(companies, start=start_date, end=end_date)
df_stocks = df.loc[:, (slice(None), companies)]
df_stacks = df_stocks.stack(level=1)
print(df_stacks.head(10))