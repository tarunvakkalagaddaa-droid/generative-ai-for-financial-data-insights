"""Streamlit dashboard: streamlit run app.py"""
import streamlit as st
import plotly.graph_objects as go
from src.data_loader import load_prices
from src.metrics import add_indicators, summarize_all
from src.insights import generate_insight

st.set_page_config(page_title="GenAI Financial Insights", layout="wide")
st.title("Generative AI for Financial Data Insights")

up = st.sidebar.file_uploader("Upload CSV (date, ticker, close)", type="csv")
df = load_prices(up if up else "data/sample_prices.csv")
if not up:
    st.sidebar.info("Using synthetic sample data.")

tickers = st.sidebar.multiselect("Tickers", sorted(df.ticker.unique()), default=sorted(df.ticker.unique())[:3])
if not tickers:
    st.stop()
df = df[df.ticker.isin(tickers)]

summary = summarize_all(df)
st.subheader("Key metrics")
st.dataframe(summary, use_container_width=True)

st.subheader("Price chart")
sel = st.selectbox("Ticker", tickers)
g = add_indicators(df[df.ticker == sel])
fig = go.Figure()
for col in ["close", "sma20", "sma50"]:
    fig.add_trace(go.Scatter(x=g.date, y=g[col], name=col))
st.plotly_chart(fig, use_container_width=True)

st.subheader("AI insights")
q = st.text_input("Ask a question (optional)", placeholder="Which stock had the best risk-adjusted return?")
if st.button("Generate insights"):
    with st.spinner("Thinking..."):
        st.markdown(generate_insight(summary, q or None))
