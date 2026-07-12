import streamlit as st
import requests 
import pandas as pd 
import plotly.express as px

import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(layout = 'wide')
st.title("Market Intelligence Platform")

with st.sidebar:
    ticker = st.text_input("Ticker")

    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

if st.button("Analyze"):
    with st.spinner("Calling API..."):
        payload = {
                    "ticker": ticker, 
                    "start_date": start_date.strftime("%Y-%m-%d"), 
                    "end_date": end_date.strftime("%Y-%m-%d")
                }
                
        response = requests.get(f"{API_URL}/market-summary", params=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Current Price", f"${data['current_price']:.2f}")
            with col2:
                st.metric(label="Annual Return", value=f"{data['annual_return']:.1%}")
            with col3:
                st.metric(label="Annualized Volatility", value=f"{data['annualized_volatility']:.1%}")
            with col4:
                st.metric("Trend", data["trend"])
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Current Drawdown", f"{data['current_drawdown']:.1%}")
            with col2:
                st.metric(label="Max Drawdown", value=f"{data['max_drawdown']:.1%}")
            with col3:
                st.metric(label="52W High", value=f"${data['52_week_high']:.2f}")
            with col4:
                st.metric(label="52W Low", value=f"${data['52_week_low']:.2f}")
            
            history_response = requests.get(
                f"{API_URL}/price-history",
                params=payload,
                timeout=10
            )

            if history_response.status_code == 200:

                history_df = pd.DataFrame(history_response.json())

                fig = px.line(
                    history_df,
                    x="Date",
                    y="Close",
                    title=f"{ticker} Price History"
                )

                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Price ($)",
                    hovermode="x unified"
                )

                st.plotly_chart(fig, use_container_width=True)

            else:
                st.error("Couldn't load price history.")

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)