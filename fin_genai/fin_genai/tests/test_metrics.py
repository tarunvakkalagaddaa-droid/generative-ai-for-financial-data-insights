import pandas as pd
from src.metrics import max_drawdown, summarize_ticker

def test_max_drawdown():
    assert max_drawdown(pd.Series([100, 120, 60, 90])) == -0.5

def test_summary_fields():
    d = pd.DataFrame({"date": pd.bdate_range("2024-01-01", periods=80),
                      "ticker": "X", "close": range(100, 180)})
    s = summarize_ticker(d)
    assert s["total_return_pct"] == 79.0 and s["trend"].startswith("above")
