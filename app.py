import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the Streamlit app title
st.title("JSE Top 40 Performance Dashboard")

# List of JSE Top 40 tickers
jse_top40 = ['BHG.JO', 'AGL.JO', 'SOL.JO', 'NPN.JO', 'CFR.JO']

# Define function to fetch data from Yahoo Finance
def fetch_jse_data(tickers, start_date="2024-03-01", end_date="2024-03-17"):
    data = {}
    for ticker in tickers:
        try:
            stock_data = yf.download(ticker, start=start_date, end=end_date)
            
            # Check if data is empty
            if stock_data.empty:
                st.warning(f"No data found for {ticker}")
            else:
                data[ticker] = stock_data

        except Exception as e:
            st.error(f"Failed to fetch data for {ticker}: {e}")

    return data

# Function to calculate daily returns
def calculate_daily_returns(data):
    daily_returns = {}
    for ticker, df in data.items():
        try:
            df['Daily Return'] = df['Close'].pct_change() * 100
            daily_returns[ticker] = df['Daily Return'].iloc[-1]
        except Exception as e:
            st.error(f"Error calculating returns for {ticker}: {e}")
    return daily_returns

# Function to plot stock performance
def plot_performance(data):
    plt.figure(figsize=(10, 6))
    for ticker, df in data.items():
        plt.plot(df['Close'], label=ticker)
    plt.legend()
    plt.title("JSE Top 40 Stock Price Trends")
    plt.xlabel("Date")
    plt.ylabel("Stock Price (ZAR)")
    st.pyplot(plt)

# Load the data
data = fetch_jse_data(jse_top40)

# Display buttons for user interaction
if st.button("Show JSE Top 40 Companies"):
    st.write("Loaded companies:", list(data.keys()))

if st.button("Show Daily Return Comparisons"):
    if data:
        daily_returns = calculate_daily_returns(data)
        returns_df = pd.DataFrame(list(daily_returns.items()), columns=["Ticker", "Daily Return (%)"])
        returns_df = returns_df.sort_values(by="Daily Return (%)", ascending=False)
        st.dataframe(returns_df)

if st.button("Rank Top Performers"):
    if data:
        daily_returns = calculate_daily_returns(data)
        sorted_stocks = sorted(daily_returns.items(), key=lambda x: x[1], reverse=True)
        st.write("Top Performers:")
        for rank, (ticker, return_) in enumerate(sorted_stocks[:5], 1):
            st.write(f"{rank}. {ticker}: {return_:.2f}%")

# Historical price view per stock
st.write("Select a stock to view its historical prices:")
selected_stock = st.selectbox("Choose a stock", jse_top40)

if selected_stock and selected_stock in data:
    st.line_chart(data[selected_stock]['Close'])
else:
    st.warning("Please select a valid stock.")

# Plot performance visualization
if st.button("Visualize Performance"):
    if data:
        plot_performance(data)
