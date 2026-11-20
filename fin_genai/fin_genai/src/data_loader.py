import pandas as pd

REQUIRED = {"date", "ticker", "close"}

def load_prices(source) -> pd.DataFrame:
    """Load a CSV path or file-like with columns: date, ticker, close[, volume]."""
    df = pd.read_csv(source, parse_dates=["date"])
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing columns: {sorted(missing)}")
    return df.sort_values(["ticker", "date"]).reset_index(drop=True)

def fetch_live(tickers, start="2024-01-01", end=None) -> pd.DataFrame:
    """Optional: pull real data with yfinance (pip install yfinance; needs internet)."""
    import yfinance as yf
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)
    close = raw["Close"] if "Close" in raw else raw
    if isinstance(close, pd.Series):
        close = close.to_frame(tickers[0] if isinstance(tickers, list) else tickers)
    out = close.reset_index().melt(id_vars="Date", var_name="ticker", value_name="close")
    return out.rename(columns={"Date": "date"}).dropna().sort_values(["ticker", "date"])
