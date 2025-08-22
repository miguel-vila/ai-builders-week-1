import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data
def get_btc_data(start, end):
    """Download and cache BTC price data"""
    return yf.download("BTC-USD", start=start, end=end, interval="1mo")['Close']

def main():
    investment_period = st.slider("Select investment period (years)", 1, 10, 5) * 12
    monthly_dca = 100
    start = '2009-01-01'
    end = '2025-08-21'
    # get btc month to month data
    btc_data = get_btc_data(start, end)
    st.title("Bitcoin Dollar Cost Averaging (DCA) Calculator")
    st.subheader("BTC value")
    st.line_chart(btc_data)
    st.write("Investment Period (Months):", investment_period)
    st.write("BTC data shape:", btc_data.shape)
    btc_per_buy = monthly_dca / btc_data
    st.write("BTC per buy shape:", btc_per_buy.shape)
    btc_accum = btc_per_buy.rolling(investment_period, min_periods=investment_period).sum()
    # remove NaN values from rolling calculation
    btc_accum = btc_accum.dropna()
    st.write("BTC accumulated shape:", btc_accum.shape)
    st.write("BTC:", btc_data)
    st.write("BTC per buy:", btc_per_buy)
    st.write("BTC Accumulated:", btc_accum)
    # st.write("BTC 2018-01-01:", btc_data['2018-01-01'])
    # st.write("Accumulated BTC 2018-01-01:", btc_accum['2018-01-01'])
    
    # Use the same index for both btc_accum and btc_data to ensure proper alignment
    st.write("btc_data[investment_period:]:", btc_data[investment_period:])
    investment_value = btc_accum * btc_data[investment_period:]
    st.write("Investment value:", investment_value)
    st.write("Investment value shape:", investment_value.shape)
    return_value = (investment_value / (investment_period * monthly_dca) - 1)
    return_value = return_value.rename(columns={'BTC-USD': "Return (%)"})
    st.write("Return value shape:", return_value.shape)
    st.write("Return value:", return_value)
    #debug dimensions
    st.write(f"BTC Accumulated: {btc_accum}")
    # investment_value = btc_accum * monthly_dca
    # cost = investment_period * monthly_dca
    st.subheader(f"Investment Return when selling after {investment_period // 12} years")
    # format return_value

    st.line_chart(return_value)


if __name__ == "__main__":
    main()
