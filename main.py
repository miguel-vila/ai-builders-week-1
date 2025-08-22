import yfinance as yf
import streamlit as st
import pandas as pd


def main():
    investment_period = st.slider("Select investment period (years)", 1, 10, 5) * 12
    monthly_dca = 100
    start = '2009-01-01'
    end = '2025-08-21'
    # get btc month to month data
    btc_data = yf.download("BTC-USD", start=start, end=end, interval="1mo")['Close']
    st.title("Bitcoin Dollar Cost Averaging (DCA) Calculator")
    st.subheader("BTC value")
    st.line_chart(btc_data)
    st.write("Investment Period (Months):", investment_period)
    st.write("BTC data shape:", btc_data.shape)
    btc_per_buy = monthly_dca / btc_data
    st.write("BTC per buy shape:", btc_per_buy.shape)
    btc_accum = btc_per_buy.rolling(investment_period, min_periods=investment_period).sum()
    # remove first investment period
    btc_accum = btc_accum[investment_period:]
    st.write("BTC accumulated shape:", btc_accum.shape)
    # investment_value = 
    investment_value = btc_accum * btc_data[investment_period:]
    st.write("Investment value shape:", investment_value.shape)
    return_value = (investment_value / (investment_period * monthly_dca) - 1)
    return_value = return_value.rename(columns={'BTC-USD': "Return (%)"})
    st.write("Return value shape:", return_value.shape)
    #debug dimensions
    st.write(f"BTC Accumulated: {btc_accum}")
    # investment_value = btc_accum * monthly_dca
    # cost = investment_period * monthly_dca
    st.subheader(f"Investment Return when selling after {investment_period // 12} years")
    # format return_value

    st.line_chart(return_value)


if __name__ == "__main__":
    main()
