"""
Batch-runs lexicon sentiment scoring + forward returns for everything
currently listed in TRANSCRIPT_LOG, and prints a combined results table.

Usage:
    python3 src/run_batch.py
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import pandas as pd
from companies import TRANSCRIPT_LOG
from sentiment_lexicon import LexiconScorer
from fetch_prices import get_forward_returns

DICT_PATH = "data/loughran_mcdonald_dict.csv"
TRANSCRIPTS_DIR = "data/transcripts"


def run_batch():
    scorer = LexiconScorer(DICT_PATH)
    rows = []

    for entry in TRANSCRIPT_LOG:
        file_path = os.path.join(TRANSCRIPTS_DIR, entry["file"])

        if not os.path.exists(file_path):
            print(f"SKIPPED — file not found: {file_path}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        sentiment = scorer.score(text)

        try:
            returns = get_forward_returns(entry["ticker"], entry["call_date"])
        except Exception as e:
            print(f"SKIPPED returns for {entry['ticker']} {entry['quarter']}: {e}")
            returns = {}

        row = {
            "ticker": entry["ticker"],
            "quarter": entry["quarter"],
            "call_date": entry["call_date"],
            "net_sentiment": sentiment["net_sentiment"],
            "positive_pct": sentiment["positive_pct"],
            "negative_pct": sentiment["negative_pct"],
            "uncertainty_pct": sentiment["uncertainty_pct"],
            "word_count": sentiment["word_count"],
            "return_1d": returns.get("return_1d"),
            "return_5d": returns.get("return_5d"),
            "return_30d": returns.get("return_30d"),
        }
        rows.append(row)
        print(f"Done: {entry['ticker']} {entry['quarter']}")

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    df = run_batch()
    print("\n--- Results ---")
    print(df.to_string(index=False))

    os.makedirs("data/processed", exist_ok=True)
    out_path = "data/processed/results.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved to {out_path}")
