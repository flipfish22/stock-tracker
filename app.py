import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Tracker",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Stock Tracker")
st.markdown("Track real-time stock prices, historical data, and key metrics.")

# ── Sidebar controls ───────────────────────────────────────────────────────────
st.sidebar.header("Settings")

ticker_input = st.sidebar.text_input(
    "Stock Ticker(s)",
    value="AAPL, MSFT, GOOGL",
    help="Enter one or more comma-separated ticker symbols (e.g. AAPL, TSLA)",
)

period_options = {
    "1 Week": "7d",
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y",
}
selected_period_label = st.sidebar.selectbox("Time Period", list(period_options.keys()), index=3)
selected_period = period_options[selected_period_label]

chart_type = st.sidebar.radio("Chart Type", ["Line", "Candlestick"], index=0)

# ── Data fetching ──────────────────────────────────────────────────────────────
tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

if not tickers:
    st.warning("Please enter at least one ticker symbol.")
    st.stop()

@st.cache_data(ttl=300)  # cache for 5 minutes
def fetch_data(ticker: str, period: str) -> pd.DataFrame:
    return yf.download(ticker, period=period, progress=False)

@st.cache_data(ttl=300)
def fetch_info(ticker: str) -> dict:
    try:
        return yf.Ticker(ticker).info
    except Exception:
        return {}

# ── Key metrics summary ────────────────────────────────────────────────────────
st.subheader("Key Metrics")
cols = st.columns(len(tickers))

for col, ticker in zip(cols, tickers):
    info = fetch_info(ticker)
    with col:
        st.metric(
            label=f"{ticker} — {info.get('shortName', ticker)}",
            value=f"${info.get('currentPrice') or info.get('regularMarketPrice', 'N/A')}",
            delta=f"{info.get('regularMarketChangePercent', 0):.2f}%" if info.get('regularMarketChangePercent') else None,
        )

st.divider()

# ── Price chart ────────────────────────────────────────────────────────────────
st.subheader(f"Price History — {selected_period_label}")

for ticker in tickers:
    df = fetch_data(ticker, selected_period)

    if df.empty:
        st.warning(f"No data found for **{ticker}**. Check the ticker symbol.")
        continue

    fig = go.Figure()

    if chart_type == "Line":
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"].squeeze(),
            mode="lines",
            name=ticker,
            line=dict(width=2),
        ))
    else:  # Candlestick
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df["Open"].squeeze(),
            high=df["High"].squeeze(),
            low=df["Low"].squeeze(),
            close=df["Close"].squeeze(),
            name=ticker,
        ))

    fig.update_layout(
        title=f"{ticker} — {chart_type} Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=(chart_type == "Candlestick"),
        height=500,
        template="plotly_dark",
    )

    st.plotly_chart(fig, use_container_width=True)

# ── Raw data table ─────────────────────────────────────────────────────────────
with st.expander("📊 View Raw Data"):
    for ticker in tickers:
        df = fetch_data(ticker, selected_period)
        if not df.empty:
            st.markdown(f"**{ticker}**")
            st.dataframe(df.tail(30).sort_index(ascending=False), use_container_width=True)

st.caption("Data provided by Yahoo Finance via yfinance. Refreshed every 5 minutes.")