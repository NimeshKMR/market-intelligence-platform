import pandas as pd 
import numpy as np 

def calculate_returns(close : pd.Series):
    returns = close.pct_change()
    return returns

def calculate_log_returns(close : pd.Series):
    log_returns = np.log(1  + close.pct_change())
    return log_returns

def moving_average(close : pd.Series, window : int):
    moving_average = close.rolling(window).mean()
    return moving_average

def rolling_volatility(returns : pd.Series, window : int):
    rolling_volatility = returns.rolling(window).std()
    return rolling_volatility

def monthly_returns(close : pd.Series):
    monthly_close = close.resample('ME').last()
    monthly_returns = monthly_close.pct_change()
    return monthly_returns 

def annual_returns(close : pd.Series):
    annual_close = close.resample('YE').last()
    annual_returns = annual_close.pct_change()
    return annual_returns 


def drawdown(close : pd.Series):
    peak = 0
    drawdown = pd.Series(np.nan, index = close.index)
    for date, price in close.items():
        if price > peak:
            peak = price 
            drawdown.loc[date] = 0
        else:
            drawdown.loc[date] = (price/peak)-1
    return drawdown

def cumulative_returns(returns : pd.Series):
    cumulative_returns = returns + 1 
    cumulative_returns = cumulative_returns.cumprod() 
    cumulative_returns = cumulative_returns-1 
    return cumulative_returns

def trend(close : pd.Series):
    trend = []
    current_price = close.iloc[-1]
    trend.append(current_price > moving_average(close, 200).iloc[-1])
    trend.append(moving_average(close, 50).iloc[-1] > moving_average(close, 200).iloc[-1])
    trend.append(calculate_returns(close).iloc[-1] > 0)
    trend.append(drawdown(close).iloc[-1] < 0.10)
    return trend 
    
def trend_map(close : pd.Series):
    trend_list = trend(close)
    tc = 0
    for x in trend_list:
        if x == True:
            tc = tc+1
    trend_mapping = {0 : "Strong Bearish",
                     1 : "Bearish",
                     2 : "Neutral",
                     3 : "Bullish",
                     4 : "Strong Bullish"}
    return trend_mapping[tc]

