from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

END = date.today()
START = date.today() - timedelta(days=365)

st.set_page_config(page_title="Stock Price Dashboard", page_icon=":bar_chart:", layout="wide")
st.title("Stock Analysis")

st.sidebar.title("Inputs")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
comparison_ticker = st.sidebar.text_input("Enter Comparison Ticker", value="SPY")
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start Date", START)
end_date = col2.date_input("End Date", END)
run_button = st.sidebar.button("Run")

@st.cache_data
def get_stock_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
    except Exception as e:
        return None, f"Error fetching data for ticker '{ticker}': {e}"
    if data.empty:
        return None, f"No data found for ticker '{ticker}' in the specified date range."
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    return data, f"Data for ticker '{ticker}' from {start_date} to {end_date} retrieved successfully."


if run_button:
    df, message = get_stock_data(ticker, start_date, end_date)
    comparison_df, comparison_message = get_stock_data(comparison_ticker, start_date, end_date)

    if df is None:
        st.error(message)
    elif comparison_df is None:
        st.error(comparison_message)
    else:
        st.success(message)

        # make both stocks start at 100 so they can be compared
        df["normalized_close"] = (df["Close"] / df["Close"].iloc[0]) * 100
        comparison_df["normalized_close"] = (comparison_df["Close"] / comparison_df["Close"].iloc[0]) * 100

        tab1, tab2 = st.tabs(["Price Chart", "📈 Comparison"])

        with tab1:
            fig = px.line(df, x=df.index, y="Close", title=f"{ticker} Closing Price")
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            compare_df = pd.DataFrame()
            compare_df[ticker] = df["normalized_close"]
            compare_df[comparison_ticker] = comparison_df["normalized_close"]

            fig4 = px.line(compare_df, labels={"value": "Normalized Price", "variable": "Ticker"}, title=f"{ticker} vs {comparison_ticker} Performance (Base 100)")
            st.plotly_chart(fig4, use_container_width=True)

            st.write("Summary Stats (normalized to 100)")
            stats_df = pd.DataFrame()
            stats_df[ticker] = [df["normalized_close"].min(), df["normalized_close"].max(), df["normalized_close"].iloc[-1]]
            stats_df[comparison_ticker] = [comparison_df["normalized_close"].min(), comparison_df["normalized_close"].max(), comparison_df["normalized_close"].iloc[-1]]
            stats_df.index = ["Min", "Max", "Final Value"]
            st.dataframe(stats_df)
