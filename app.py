import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="JSE Top 40 Performance Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data(tickers):
    data = {ticker: yf.download(ticker, period='7d', interval='1d') for ticker in tickers}
    return data

# Define JSE Top 40 companies (using placeholder tickers)
jse_top40 = ['NPN.JO', 'MTN.JO', 'SOL.JO', 'BHP.JO', 'ABG.JO']  # Add more tickers

# Heading
st.title("📈 JSE Top 40 Performance Dashboard")

# Button 1: Show JSE Top 40 Firms
if st.button("Show JSE Top 40 Firms"):
    st.write("### JSE Top 40 Companies")
    st.write(pd.DataFrame({'Company': jse_top40}))

# Button 2: Show Daily Returns
if st.button("Show Daily Return Comparisons"):
    data = load_data(jse_top40)
    daily_returns = {ticker: ((data[ticker]['Close'].iloc[-1] - data[ticker]['Close'].iloc[-2]) / data[ticker]['Close'].iloc[-2]) * 100 for ticker in jse_top40}
    returns_df = pd.DataFrame.from_dict(daily_returns, orient='index', columns=['Daily Return (%)']).sort_values(by='Daily Return (%)', ascending=False)
    st.bar_chart(returns_df)

# Button 3: Show Top Performers
if st.button("Show Top Performers"):
    data = load_data(jse_top40)
    performance_df = pd.DataFrame({
        'Company': jse_top40,
        'Last Price': [data[ticker]['Close'].iloc[-1] for ticker in jse_top40],
        'Daily Return (%)': [(data[ticker]['Close'].iloc[-1] - data[ticker]['Close'].iloc[-2]) / data[ticker]['Close'].iloc[-2] * 100 for ticker in jse_top40]
    }).sort_values(by='Daily Return (%)', ascending=False)
    st.write("### Top Performing Stocks")
    st.dataframe(performance_df)

    # Allow clicking individual stocks
    stock_choice = st.selectbox("Select a stock to view historical prices:", performance_df['Company'])
    if stock_choice:
        st.line_chart(data[stock_choice]['Close'])

# Styling
st.markdown("""
    <style>
        .stButton button { background-color: #4CAF50; color: white; font-size: 18px; border-radius: 8px; }
        .stTitle { color: #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

st.write("---")
st.write("📍 *Powered by Yahoo Finance and Streamlit*")
