import yfinance as yf
import datetime as dt
import pandas as pd
import os

pd.set_option('display.max_columns', None) 
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')

if os.path.exists("raw_stock_data.csv"):
    existing_df = pd.read_csv("raw_stock_data.csv")
    last_date = pd.to_datetime(existing_df["Date"]).max()
    start_date = (last_date + dt.timedelta(days=1)).date()
else:
    existing_df = None
    start_date = "2025-01-01"

end_date = dt.date.today() + dt.timedelta(days=1)

if start_date < end_date:
    all_tickers = ["RELIANCE.NS", "IOC.NS", "BPCL.NS", "HINDPETRO.NS", "BZ=F", "USDINR=X"]
    df = yf.download(all_tickers, start=start_date, end=end_date)
    
    if not df.empty:
        companies = ["RELIANCE.NS", "IOC.NS", "BPCL.NS", "HINDPETRO.NS"]
        df_stocks = df.loc[:, (slice(None), companies)]
        df_stacks = df_stocks.stack(level=1)
        
        brent_close = df["Close"]["BZ=F"].ffill().bfill()
        usdinr_close = df["Close"]["USDINR=X"].ffill().bfill()
        
        df_stacks["Brent_Crude"] = df_stacks.index.get_level_values("Date").map(brent_close)
        df_stacks["USD_INR"] = df_stacks.index.get_level_values("Date").map(usdinr_close)
        
        df_flat = df_stacks.reset_index()
        df_flat["Daily_Change"] = df_flat["Close"] - df_flat["Open"]
        
        if existing_df is not None:
            combined_df = pd.concat([existing_df, df_flat], ignore_index=True)
        else:
            combined_df = df_flat
            
        combined_df = combined_df.drop_duplicates(subset=["Date", "Ticker"], keep="last")
        
        combined_df.to_csv("raw_stock_data.csv", index=False)
        
        rounded_df = combined_df.copy()
        numeric_cols = ["Close", "High", "Low", "Open", "Volume", "Brent_Crude", "USD_INR", "Daily_Change"]
        rounded_df[numeric_cols] = rounded_df[numeric_cols].round(3)
        rounded_df.to_csv("cleaned_stock_data.csv", index=False)
        
        print(f"Successfully updated! Total rows now in file: {len(combined_df)}")
        print(rounded_df.tail(10))
else:
    print("Already up to date!")
