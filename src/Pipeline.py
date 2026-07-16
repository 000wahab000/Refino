# pyrefly: ignore [missing-import]
import yfinance as yf
import datetime as dt

start_date = "2025-01-01"
end_date = dt.date.today()
tickers = ["RELIANCE.NS","IOCL.NS","BPCL.NS","HPCL.NS","BZ=F","USDINR=X"]

# A list containing the tickers for our 4 companies + 2 macro indicators
tickers = ["RELIANCE.NS", "IOC.NS", "BPCL.NS", "HINDPETRO.NS", "BZ=F", "USDINR=X"]


# Download data for all tickers
df = yf.download(tickers, start=start_date, end=end_date)
df.to_csv("stock_data.csv")
print(df.head())    
