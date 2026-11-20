# Generative AI for Financial Data Insights

Computes financial metrics (returns, volatility, Sharpe, drawdown, RSI, moving averages) from price data,
then uses a generative AI model (Claude) to explain them in plain language.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env        # add ANTHROPIC_API_KEY (optional)
python -m src.generate_sample_data   # only if data/sample_prices.csv is missing
```

## Run
```bash
python main.py --question "Which ticker is riskiest?"   # CLI
streamlit run app.py                                     # dashboard
pytest                                                   # tests
```

Without an API key, a rule-based offline summary is used so everything still runs.
Sample data is synthetic. CSV format: `date,ticker,close[,volume]`.
`src/data_loader.py` has an optional `fetch_live()` for real data via yfinance.

## Structure
- `src/data_loader.py` load/validate data · `src/metrics.py` indicators · `src/insights.py` GenAI layer
- `app.py` Streamlit UI · `main.py` CLI · `tests/` unit tests

_Educational project; not investment advice._
