###streamlit_app
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils import get_stock_data, get_crypto_data, get_company_news, get_fundamentals

st.set_page_config(page_title="Tiingo Financial Dashboard", layout="wide")

# Sidebar
st.sidebar.title("Tiingo Financial Dashboard")
analysis_type = st.sidebar.selectbox(
    "Select Analysis Type",
    ["Stocks", "Crypto", "News", "Fundamentals"]
)

# Main content
st.title(f"Tiingo {analysis_type} Analysis")

if analysis_type == "Stocks":
    # Stock Analysis Section
    ticker = st.text_input("Enter Stock Ticker", value="AAPL").upper()
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=365)
        )
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    if st.button("Get Stock Data"):
        data = get_stock_data(ticker, start_date, end_date)
        if data is not None:
            # Create stock price chart
            fig = go.Figure(data=[go.Candlestick(x=data['date'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'])])
            
            fig.update_layout(title=f"{ticker} Stock Price",
                            xaxis_title="Date",
                            yaxis_title="Price")
            st.plotly_chart(fig, use_container_width=True)
            
            # Display statistics
            st.subheader("Statistics")
            stats = {
                "Average Volume": data['volume'].mean(),
                "Average Close": data['close'].mean(),
                "Highest Price": data['high'].max(),
                "Lowest Price": data['low'].min()
            }
            st.write(stats)

elif analysis_type == "Crypto":
    crypto_tickers = st.text_input("Enter Crypto Tickers (comma-separated)", value="btcusd").upper()
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=30)
        )
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    if st.button("Get Crypto Data"):
        tickers = [t.strip() for t in crypto_tickers.split(",")]
        data = get_crypto_data(tickers, start_date, end_date)
        if data is not None:
            # Create price chart
            fig = go.Figure()
            for ticker in tickers:
                ticker_data = data[data['ticker'] == ticker]
                fig.add_trace(go.Scatter(
                    x=ticker_data['date'],
                    y=ticker_data['close'],
                    mode='lines',
                    name=f'{ticker} Close Price'
                ))
            fig.update_layout(
                title="Cryptocurrency Prices",
                xaxis_title="Date",
                yaxis_title="Price",
                legend_title="Cryptocurrencies"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Display raw data
            st.subheader("Raw Data")
            st.dataframe(data)

elif analysis_type == "News":
    ticker = st.text_input("Enter Ticker for News (optional)")
    limit = st.slider("Number of News Articles", 5, 50, 10)
    
    if st.button("Get News"):
        news_data = get_company_news(tickers=[ticker] if ticker else None, limit=limit)
        if news_data is not None:
            for _, article in news_data.iterrows():
                st.subheader(article['title'])
                st.write(f"Source: {article['source']}")
                st.write(f"Published: {article['publishedDate']}")
                st.write(article['description'])
                st.markdown("---")

elif analysis_type == "Fundamentals":
    ticker = st.text_input("Enter Stock Ticker for Fundamentals", value="AAPL").upper()
    
    if st.button("Get Fundamentals"):
        fund_data = get_fundamentals(ticker)
        if fund_data is not None:
            st.dataframe(fund_data)

st.sidebar.markdown("---")
st.sidebar.markdown("Data provided by [Tiingo](https://www.tiingo.com)")
