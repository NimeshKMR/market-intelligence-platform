import yfinance as yf 
import pandas as pd 
import matplotlib.pyplot as plt 

def download_asset(ticker : str, start_date : str, end_date : str):
    df = yf.download(ticker, start = start_date, end = end_date)
    df.columns = df.columns.droplevel(1)
    df = df[["Close", "Volume"]]
    if df.empty:
        raise ValueError(f"No data found for {ticker}")
    return df

def download_assets(tickers : list[str], start_date : str, end_date : str):
    assets = {}
    for ticker in tickers:
        assets[ticker] = download_asset(ticker, start_date, end_date)
    return assets   

def align_assets(assets : dict):
    combined_data = pd.concat(objs = assets, axis = 1)
    return combined_data 
