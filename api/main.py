from fastapi import FastAPI 
from market_intelligence.data.market.yahoo import download_asset, download_assets, align_assets
from market_intelligence.market_analytics.market_summary import market_summary, compare_assets, correlation_analysis, period_analysis
import pandas as pd 

api = FastAPI()

@api.get("/")
def root():
    return {
        "message" : "Market Intelligence Platform API"
    }

@api.get("/assets")
def download(ticker : str, start_date : str, end_date : str):
    df = download_asset(ticker, start_date, end_date)
    return{
        "ticker" : ticker,
        "rows" : df.shape[0],
        "columns" : list(df.columns),
        "start_date" : df.index[0],
        "end_date" : df.index[-1]
    }

@api.get("/price-history")
def price_history(ticker : str, start_date : str, end_date : str):
    df = download_asset(ticker, start_date, end_date)
    df = df.drop(columns = 'Volume')
    return df.reset_index().to_dict(orient="records")


@api.get("/market-summary")
def summary(ticker : str, start_date : str, end_date : str):
    df = download_asset(ticker, start_date, end_date)
    return market_summary(df)

@api.get("/compare-assets")
def compare(tickers : str, start_date : str, end_date : str):
    ticker_list = tickers.split(',')
    assets = download_assets(ticker_list, start_date, end_date)
    return compare_assets(assets)

@api.get("/correlation")
def correlation(tickers : str, start_date : str, end_date : str):
    ticker_list = tickers.split(',')
    assets = download_assets(ticker_list, start_date, end_date)
    aligned = align_assets(assets)
    return correlation_analysis(aligned)

@api.get("/period-analysis")
def period(ticker : str, start_date : str, end_date : str):
    df = download_asset(ticker, start_date, end_date)
    return period_analysis(df, start_date, end_date)