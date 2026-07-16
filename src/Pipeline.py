# pyrefly: ignore [missing-import]
import yfinance as yf
import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None) 
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')

start_date = "2025-01-01"
end_date = dt.date.today()

all_tickers = ["RELIANCE.NS", "IOC.NS", "BPCL.NS", "HINDPETRO.NS", "BZ=F", "USDINR=X"]
df = yf.download(all_tickers, start=start_date, end=end_date)

companies = ["RELIANCE.NS", "IOC.NS", "BPCL.NS", "HINDPETRO.NS"]
df_stocks = df.loc[:, (slice(None), companies)]
df_stacks = df_stocks.stack(level=1)

brent_close = df["Close"]["BZ=F"].ffill()
usdinr_close = df["Close"]["USDINR=X"].ffill()

df_stacks["Brent_Crude"] = df_stacks.index.get_level_values("Date").map(brent_close)
df_stacks["USD_INR"] = df_stacks.index.get_level_values("Date").map(usdinr_close)

df_flat = df_stacks.reset_index()
df_flat["Daily_Change"] = df_flat["Close"] - df_flat["Open"]

combined_df = df_flat.drop_duplicates(subset=["Date", "Ticker"], keep="last")

combined_df.to_csv("raw_stock_data.csv", index=False)

rounded_df = combined_df.round(3)
rounded_df.to_csv("cleaned_stock_data.csv", index=False)
print(f"Successfully updated! Total rows now in file: {len(combined_df)}")