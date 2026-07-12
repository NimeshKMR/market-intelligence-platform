import streamlit as st
import requests
import pandas as pd
import plotly.express as px

import os

API_URL = os.getenv("API_URL", "http://localhost:8000")
st.write(f"API_URL = {API_URL}")
st.title("Asset Comparison")

with st.sidebar:
    with st.form("compare_form"):

        tickers = st.text_input(
            "Tickers (comma separated)",
            value="SPY,GLD,^TNX"
        )

        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")

        submitted = st.form_submit_button("Compare")

if not submitted:
    st.stop()

payload = {
    "tickers": tickers,
    "start_date": start_date.strftime("%Y-%m-%d"),
    "end_date": end_date.strftime("%Y-%m-%d")
}

# =============================
# Comparison Table
# =============================
compare_response = requests.get(
    f"{API_URL}/compare-assets",
    params=payload,
    timeout=10
)

if compare_response.status_code != 200:
    st.error(f"API Error: {compare_response.status_code}")
    st.code(compare_response.text)
    st.stop()

data = compare_response.json()
df = pd.DataFrame(data).T
numeric_columns = [
    "current_price",
    "annual_return",
    "annualized_volatility",
    "current_drawdown",
    "max_drawdown",
    "52_week_high",
    "52_week_low",
    "avg_volume"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col])

st.subheader("Comparison Table")

st.dataframe(
    df.style.format({
        "current_price": "${:,.2f}",
        "annual_return": "{:.1%}",
        "annualized_volatility": "{:.1%}",
        "current_drawdown": "{:.1%}",
        "max_drawdown": "{:.1%}",
        "52_week_high": "${:,.2f}",
        "52_week_low": "${:,.2f}",
        "avg_volume": "{:,.0f}"
    })
)

# =============================
# Performance Chart
# =============================

st.subheader("Normalized Performance Comparison")
fig = px.line()

for ticker in tickers.split(","):

    history_response = requests.get(
        f"{API_URL}/price-history",
        params={
            "ticker": ticker.strip(),
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        },
        timeout=10
    )

    if history_response.status_code != 200:
        st.warning(f"Couldn't load {ticker.strip()}")
        continue

    history = pd.DataFrame(history_response.json())

    if history.empty:
        continue

    history["Close"] = history["Close"] / history["Close"].iloc[0] * 100

    fig.add_scatter(
        x=history["Date"],
        y=history["Close"],
        mode="lines",
        name=ticker.strip()
    )

fig.update_layout(
    title="Growth of $100 Investment",
    xaxis_title="Date",
    yaxis_title="Normalized Value"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# Correlation Matrix
# =============================

st.subheader("Correlation Matrix")
corr_response = requests.get(
    f"{API_URL}/correlation",
    params=payload,
    timeout=10
)

if corr_response.status_code != 200:
    st.error("Couldn't load correlation matrix.")
    st.stop()

corr_df = pd.DataFrame(corr_response.json())
fig = px.imshow(
    corr_df,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    aspect="auto",
    title="Asset Correlation Matrix"
)

fig.update_layout(
    xaxis_title="",
    yaxis_title=""
)

st.plotly_chart(fig, use_container_width=True)