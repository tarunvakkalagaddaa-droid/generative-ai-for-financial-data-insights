"""CLI: python main.py [--csv data/sample_prices.csv] [--question "..."]"""
import argparse
from src.data_loader import load_prices
from src.metrics import summarize_all
from src.insights import generate_insight

p = argparse.ArgumentParser()
p.add_argument("--csv", default="data/sample_prices.csv")
p.add_argument("--question", default=None)
a = p.parse_args()

summary = summarize_all(load_prices(a.csv))
print(summary.to_string(index=False), "\n")
print(generate_insight(summary, a.question))
