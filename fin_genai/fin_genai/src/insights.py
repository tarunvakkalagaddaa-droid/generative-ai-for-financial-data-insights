"""Generative AI layer: turns computed metrics into plain-language insights."""
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

SYSTEM = (
    "You are a careful financial data analyst. Use ONLY the metrics provided. "
    "Do not invent numbers or give personalised investment advice. "
    "Be concise: a short overview, then bullets per ticker (performance, risk, momentum), "
    "then key caveats."
)

def _table(summary: pd.DataFrame) -> str:
    return summary.to_markdown(index=False) if _has_tabulate() else summary.to_string(index=False)

def _has_tabulate() -> bool:
    try:
        import tabulate  # noqa: F401
        return True
    except ImportError:
        return False

def offline_insight(summary: pd.DataFrame) -> str:
    """Rule-based fallback so the project works without an API key."""
    best = summary.loc[summary.total_return_pct.idxmax()]
    worst = summary.loc[summary.total_return_pct.idxmin()]
    riskiest = summary.loc[summary.annual_volatility_pct.idxmax()]
    lines = [
        f"**Overview:** {len(summary)} tickers analysed ({summary.start.min()} to {summary.end.max()}).",
        f"- Best performer: **{best.ticker}** ({best.total_return_pct:+.1f}%).",
        f"- Weakest performer: **{worst.ticker}** ({worst.total_return_pct:+.1f}%).",
        f"- Most volatile: **{riskiest.ticker}** ({riskiest.annual_volatility_pct:.1f}% annualised).",
    ]
    for _, r in summary.iterrows():
        flag = ""
        if r.rsi14 is not None:
            flag = " RSI suggests overbought." if r.rsi14 > 70 else " RSI suggests oversold." if r.rsi14 < 30 else ""
        lines.append(f"- {r.ticker}: {r.total_return_pct:+.1f}% return, max drawdown {r.max_drawdown_pct:.1f}%, "
                     f"Sharpe {r.sharpe}, currently {r.trend}.{flag}")
    lines.append("\n_Offline summary (no API key set). Not investment advice._")
    return "\n".join(lines)

def generate_insight(summary: pd.DataFrame, question: str | None = None) -> str:
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return offline_insight(summary)
    import anthropic
    client = anthropic.Anthropic(api_key=key)
    task = question or "Summarise the key insights from these metrics."
    msg = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
        max_tokens=1000,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Metrics:\n{_table(summary)}\n\nTask: {task}"}],
    )
    return msg.content[0].text
