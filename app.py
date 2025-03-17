import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="JSE Top 40 Performance Dashboard", layout="wide")

# Load data function
def load_data(tickers):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')  # Get more days to avoid missing data
    data = {}

    for ticker in jse_top40:
        try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        if stock_data.empty:
            st.warning(f"No data found for {ticker}")
        else:
            data[ticker] = stock_data
    except Exception as e:
        st.error(f"Failed to fetch data for {ticker}: {e}")
    return data

# Define JSE Top 40 companies (using placeholder tickers)
jse_top40 = ['BHG.JO', 'AGL.JO', 'SOL.JO']  # Ensure your ticker symbols are correct

data = {}
# Heading
st.title("📈 JSE Top 40 Performance Dashboard")

# Button 1: Show JSE Top 40 Firms
if st.button("Show JSE Top 40 Firms"):
    st.write("### JSE Top 40 Companies")
    st.write(pd.DataFrame({'Company': jse_top40}))

# Button 2: Show Daily Returns

# Button: Show Daily Returns Comparison
if st.button("Show Daily Return Comparisons"):
    data = load_data(jse_top40)
    daily_returns = {}

   # Loop through tickers and fetch data
for ticker in jse_top40:
    try:
        stock_data = yf.download(ticker, start="2024-03-01", end="2024-03-17")
        
        # Check if data is empty
        if stock_data.empty:
            st.warning(f"No data found for {ticker}")
        else:
            data[ticker] = stock_data

    except Exception as e:
        st.error(f"Failed to fetch data for {ticker}: {e}")

    # Display returns if data exists
    if daily_returns:
        returns_df = pd.DataFrame.from_dict(
            daily_returns, orient='index', columns=['Daily Return (%)']
        ).sort_values(by='Daily Return (%)', ascending=False)

        st.bar_chart(returns_df)
    else:
        st.error("No valid data available for return comparisons.")


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
