"""Create a synthetic price dataset (NOT real market data) for demo purposes."""
import numpy as np
import pandas as pd
from pathlib import Path

def main(out="data/sample_prices.csv"):
    rng = np.random.default_rng(42)
    dates = pd.bdate_range("2024-01-01", "2025-12-31")
    params = {  # ticker: (start price, daily drift, daily vol)
        "AAA": (100, 0.0006, 0.012),
        "BBB": (50, 0.0002, 0.020),
        "CCC": (200, 0.0004, 0.015),
        "DDD": (30, -0.0003, 0.025),
        "EEE": (75, 0.0008, 0.018),
    }
    rows = []
    for t, (p0, mu, sig) in params.items():
        rets = rng.normal(mu, sig, len(dates))
        close = p0 * np.exp(np.cumsum(rets))
        vol = rng.integers(1_000_000, 5_000_000, len(dates))
        rows.append(pd.DataFrame({"date": dates, "ticker": t, "close": close.round(2), "volume": vol}))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    pd.concat(rows).to_csv(out, index=False)
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
