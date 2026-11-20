import numpy as np
import pandas as pd

TRADING_DAYS = 252

def add_indicators(g: pd.DataFrame) -> pd.DataFrame:
    """g: single-ticker frame sorted by date. Adds returns, SMAs and RSI."""
    g = g.copy()
    g["return"] = g["close"].pct_change()
    g["sma20"] = g["close"].rolling(20).mean()
    g["sma50"] = g["close"].rolling(50).mean()
    delta = g["close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    g["rsi14"] = 100 - 100 / (1 + gain / loss.replace(0, np.nan))
    return g

def max_drawdown(close: pd.Series) -> float:
    peak = close.cummax()
    return float((close / peak - 1).min())

def summarize_ticker(g: pd.DataFrame) -> dict:
    g = add_indicators(g)
    r = g["return"].dropna()
    vol = r.std() * np.sqrt(TRADING_DAYS)
    ann_ret = r.mean() * TRADING_DAYS
    last = g.iloc[-1]
    return {
        "ticker": g["ticker"].iloc[0],
        "start": g["date"].iloc[0].strftime("%Y-%m-%d"),
        "end": g["date"].iloc[-1].strftime("%Y-%m-%d"),
        "last_close": round(float(last["close"]), 2),
        "total_return_pct": round(float(g["close"].iloc[-1] / g["close"].iloc[0] - 1) * 100, 2),
        "annual_volatility_pct": round(float(vol) * 100, 2),
        "sharpe": round(float(ann_ret / vol), 2) if vol else None,
        "max_drawdown_pct": round(max_drawdown(g["close"]) * 100, 2),
        "rsi14": None if pd.isna(last["rsi14"]) else round(float(last["rsi14"]), 1),
        "trend": "above 50-day average" if last["close"] > last["sma50"] else "below 50-day average",
    }

def summarize_all(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([summarize_ticker(g) for _, g in df.groupby("ticker")])
