import pandas as pd 
import numpy as np 
from market_analytics.indicators import calculate_returns, annual_returns, drawdown, rolling_volatility, moving_average, trend_map, monthly_returns

def market_summary(asset: pd.DataFrame):
    if asset.empty:
        raise ValueError("Asset dataframe is empty.")
    close = asset["Close"]
    current_price = close.iloc[-1]
    returns = calculate_returns(close)
    daily_return = returns.iloc[-1]
    years = (close.index[-1] - close.index[0]).days / 365.25
    if years > 0:
        annual_return = (close.iloc[-1] / close.iloc[0]) ** (1 / years) - 1
    else:
        annual_return = None
    drawdown_series = drawdown(close)
    current_drawdown = drawdown_series.iloc[-1]
    max_drawdown = drawdown_series.min()
    avg_volume = asset["Volume"].mean()
    year_high = close.tail(252).max()
    year_low = close.tail(252).min()
    annual_volatility = returns.std() * np.sqrt(252)

    trend = trend_map(close)

    output = {
        "current_price": current_price,
        "daily_return": daily_return,
        "annual_return": annual_return,
        "current_drawdown": current_drawdown,
        "max_drawdown": max_drawdown,
        "52_week_high": year_high,
        "52_week_low": year_low,
        "annualized_volatility": annual_volatility,
        "avg_volume": avg_volume,
        "trend": trend
    }

    for key, value in output.items():
        if pd.isna(value):
            output[key] = None

    return output

def period_analysis(asset : pd.DataFrame, start : str, end : str):
    asset = asset.loc[start:end]
    close = asset['Close']
    returns = calculate_returns(close)
    end_price = close.iloc[-1]
    start_price = close.iloc[0]
    period_return = (end_price - start_price)/start_price
    annual_volatility = rolling_volatility(returns, 252).iloc[-1]
    drawdown_series = drawdown(close)
    max_drawdown = drawdown_series.min()
    best_day = returns.idxmax()
    worst_day = returns.idxmin()
    trend_map = trend_map(close)
    output = {
            "start_date": start,
        "end_date": end,
        "start_price": start_price,
        "end_price": end_price,
        "period_return": period_return,
        "annualized_volatility": annual_volatility,
        "max_drawdown": max_drawdown,
        "best_day": best_day,
        "worst_day": worst_day,
        "trend": trend_map
    }

    return output

def best_months(close : pd.Series, top_n : int):
    monthly = monthly_returns(close).sort_values(ascending = False)
    monthly.index = monthly.index.strftime("%Y-%m")
    return monthly.iloc[0:top_n]

def worst_months(close : pd.Series, top_n : int):
     monthly = monthly_returns(close).sort_values()
     monthly.index = monthly.index.strftime("%Y-%m")
     return monthly.iloc[0:top_n]

def correlation_analysis(aligned : pd.DataFrame):
    returns = calculate_returns(aligned.xs('Close', axis = 1, level = 'Price'))
    return returns.corr()

def compare_assets(assets : dict[str, pd.DataFrame]):
    output = {}
    for ticker, df in assets.items():
        output[ticker] = market_summary(df)
    return output 





