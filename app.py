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

# Function to calculate RSI
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Function to calculate MACD
def calculate_macd(data):
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

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
    
    # Calculate and show RSI
    data[selected_stock]['RSI'] = calculate_rsi(data[selected_stock])
    st.line_chart(data[selected_stock]['RSI'], use_container_width=True)

    # Calculate and show MACD
    macd, signal = calculate_macd(data[selected_stock])
    plt.figure(figsize=(10, 4))
    plt.plot(macd, label='MACD', color='blue')
    plt.plot(signal, label='Signal', color='orange')
    plt.legend()
    st.pyplot(plt)

# Generate Performance Heatmap
if st.button("Generate Performance Heatmap"):
    returns_df = pd.DataFrame({ticker: data[ticker]['Daily Return'] for ticker in jse_top40})
    plt.figure(figsize=(10, 6))
    sns.heatmap(returns_df.corr(), annot=True, cmap='coolwarm')
    st.pyplot(plt)

# Export data to CSV
if st.button("Export Data to CSV"):
    combined_data = pd.concat([data[ticker]['Close'] for ticker in jse_top40], axis=1)
    combined_data.columns = jse_top40
    combined_data.to_csv('jse_top40_data.csv')
    st.success("Data exported to CSV successfully!")

# Performance visualization
if st.button("Visualize Performance"):
    plt.figure(figsize=(10, 6))
    for ticker, df in data.items():
        plt.plot(df['Close'], label=ticker)
    plt.legend()
    plt.title("JSE Top 40 Stock Price Trends")
    plt.xlabel("Date")
    plt.ylabel("Stock Price (ZAR)")
    st.pyplot(plt)
