import pandas as pd
import numpy as np 
from market_intelligence.features.market_features import moving_average, drawdown 
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt 

def calculate_features(asset : pd.DataFrame) -> pd.DataFrame:
    if asset.empty:
        raise ValueError("Asset dataframe is empty!")
    returns = asset['Close'].pct_change()
    weekly = asset['Close'].pct_change(5)
    monthly = asset['Close'].pct_change(21)
    current_volatility = returns.rolling(20).std() * np.sqrt(252)
    mediumterm_volatility = returns.rolling(60).std() * np.sqrt(252)
    short_trend = moving_average(asset['Close'], 20)/moving_average(asset['Close'], 50)
    long_trend = moving_average(asset['Close'], 50)/moving_average(asset['Close'], 200)
    bull_bear = asset['Close']/moving_average(asset['Close'], 200)
    drawdown_series = drawdown(asset['Close'])
    current_drawdown = drawdown_series
    max_drawdown = drawdown_series.rolling(60).min()

    features = pd.DataFrame({'Weekly_Returns' : weekly, 'Monthly_Returns' : monthly
    , 'annualized_volatility_20' : current_volatility, 'annualized_volatility_60' : mediumterm_volatility, 
    'MA20/MA50' : short_trend, 'MA50/MA200' : long_trend, 'Current/MA200' : bull_bear,
    'Current Drawdown' : current_drawdown, 'Max Drawdown' : max_drawdown})
    
    return features

def prepare_features(features : pd.DataFrame) -> pd.DataFrame:
    features = features.dropna()
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    return features, scaler, scaled 

def train_regime_model(features : pd.DataFrame):
    model = KMeans(n_clusters=3, random_state=67, n_init=10)
    labels = model.fit_predict(features)
    return model, labels

def analyze_regimes(features : pd.DataFrame, labels : np.ndarray):
    features["Regime"] = labels 
    analyze = features.groupby("Regime").mean() 
    return analyze 

def plot_regimes(asset : pd.DataFrame, features : pd.DataFrame, labels : np.ndarray):
    asset = asset.loc[features.index[0] : features.index[-1]].copy()
    asset["Regime"] = labels
    colors = {
    0: "orange",
    1: "red",
    2: "green"}
    plt.figure(figsize=(14, 6))

    for i in range(len(asset) - 1):

        x = [asset.index[i], asset.index[i+1]]

        y = [asset["Close"].iloc[i], asset["Close"].iloc[i+1]]

        regime = asset["Regime"].iloc[i]

        plt.plot(x, y, color=colors[regime])
        
    plt.title("Market Regimes")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

def find_similar_periods(scaled_features, features, query_date = None, k = 5):
    model = NearestNeighbors() 
    model.fit(scaled_features)
    if query_date is None:
        row = len(features) - 1
    else:
        row = features.index.get_loc(query_date)
    query_vector = scaled_features[row]
    query_vector = query_vector.reshape(1,-1)
    distances, indices = model.kneighbors(query_vector, n_neighbors=k+1)
    indices = indices[0]
    distances = distances[0]
    similar_periods = pd.DataFrame({'Similar Date' : features.index[indices[1:]], 'Distance' : distances[1:]})
    return similar_periods

