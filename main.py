import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data
def get_btc_data(start, end):
    """Download and cache BTC price data"""
    return yf.download("BTC-USD", start=start, end=end, interval="1mo")['Close']

def main():
    global debug
    debug = False
    monthly_dca = 100
    start = '2009-01-01'
    end = '2025-08-21'
    # get btc month to month data
    btc_data = get_btc_data(start, end)
    st.title("Bitcoin Dollar Cost Averaging (DCA) Calculator")
    investment_period = st.slider("Select investment period (years)", 1, 10, 5) * 12
    st.write(f"What would be your return if you bought ${monthly_dca} of BTC every month for {investment_period // 12} years and sold all of it? * Not adjusted for inflation.")
    
    st.subheader("BTC value")
    st.line_chart(btc_data)
    btc_per_buy = monthly_dca / btc_data
    btc_accum = btc_per_buy.rolling(investment_period, min_periods=investment_period).sum()
    # remove NaN values from rolling calculation
    btc_accum = btc_accum.dropna()
    
    # Use BTC price from the following month for the investment value
    investment_value = btc_accum * btc_data.shift(-1)
    
    # The shift operation will introduce a NaN for the last value, so we drop it
    investment_value = investment_value.dropna()
    return_value = (investment_value / (investment_period * monthly_dca) - 1) * 100
    return_value = return_value.rename(columns={'BTC-USD': "Return (%)"})
    st.subheader(f"Investment Return when selling after {investment_period // 12} years")
    st.line_chart(return_value)

if __name__ == "__main__":
    main()
