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
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start Date", START)
end_date = col2.date_input("End Date", END)
mv_avg = st.sidebar.slider("Moving Average Window", min_value=1, max_value=100, value=50, step=1)

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

