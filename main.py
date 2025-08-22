import yfinance as yf
import streamlit as st
import pandas as pd

@st.cache_data
def get_btc_data(start, end):
    """Download and cache BTC price data"""
    return yf.download("BTC-USD", start=start, end=end, interval="1mo")['Close']

def main():
    st.set_page_config(page_title="BTC DCA Calculator", page_icon="₿", layout="wide")
    start = '2009-01-01'
    end = '2025-08-21'
    # get btc month to month data
    btc_data = get_btc_data(start, end)
    st.title("Bitcoin Dollar Cost Averaging (DCA) Calculator")
    
    # Sidebar controls
    st.sidebar.header("⚙️ Settings")
    investment_years = st.sidebar.slider("Investment Period (years)", 1, 10, 1)
    investment_period = investment_years * 12
    monthly_dca = st.sidebar.number_input("Monthly Investment ($)", min_value=1, max_value=10000, value=100, step=25)
    
    st.write(f"**Scenario:** Invest ${monthly_dca:,} monthly for {investment_years} years, then sell everything")
    st.caption("*Returns not adjusted for inflation or fees")
    
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
    return_value.index.name = "Sell Date"
    
    st.subheader(f"Rolling {investment_period // 12}-Year DCA Returns")
    st.line_chart(return_value)
    
    # Calculate stats
    total_invested = investment_period * monthly_dca
    median_return = return_value.median()['Return (%)']
    max_return = return_value.max()['Return (%)']
    min_return = return_value.min()['Return (%)']

    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Invested", f"${total_invested:,.0f}")
    with col2:
        st.metric("Median Return", f"{median_return:.2f}%")
    with col3:
        st.metric("Max Return", f"{max_return:.2f}%")
    with col4:
        st.metric("Min Return", f"{min_return:.2f}%")

    # Add percentile analysis
    st.subheader("Return Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        percentiles = [10, 25, 50, 75, 90]
        perc_values = [return_value.quantile(p/100)['Return (%)'] for p in percentiles]
        perc_df = pd.DataFrame({
            'Percentile': [f'{p}th' for p in percentiles],
            'Return (%)': [f'{v}%' for v in perc_values]
        })
        st.dataframe(perc_df, hide_index=True)
    
    with col2:
        positive_returns = (return_value > 0).sum()
        total_periods = len(return_value)
        win_rate = (positive_returns / total_periods * 100)['Return (%)'] if total_periods > 0 else 0
        
        st.metric("Positive Return Rate", f"{win_rate}%")
        st.metric("Total Periods Analyzed", f"{total_periods}")
        
if __name__ == "__main__":
    main()
