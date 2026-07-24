"""
Pulls historical price data and computes forward returns around a given call date.

Usage:
    from fetch_prices import get_forward_returns
    returns = get_forward_returns("TGT", "2025-05-21")
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def get_forward_returns(ticker: str, call_date: str) -> dict:
    """
    Returns 1-day, 5-day, and 30-day forward returns following an earnings call date.

    ticker: stock symbol, e.g. "TGT"
    call_date: string "YYYY-MM-DD" — the date of the earnings call
    """
    call_dt = datetime.strptime(call_date, "%Y-%m-%d")
    start = call_dt - timedelta(days=5)
    end = call_dt + timedelta(days=40)

    hist = yf.Ticker(ticker).history(start=start, end=end)
    if hist.empty:
        raise ValueError(f"No price data returned for {ticker} around {call_date}")

    hist.index = hist.index.tz_localize(None)  # strip timezone for comparison

    # find the first trading day on or after the call date
    future_dates = hist.index[hist.index >= call_dt]
    if len(future_dates) == 0:
        raise ValueError(f"No trading days found after {call_date} for {ticker}")

    base_date = future_dates[0]
    base_price = hist.loc[base_date, "Close"]

    def price_n_days_later(n):
        target_dates = hist.index[hist.index >= base_date + timedelta(days=n)]
        if len(target_dates) == 0:
            return None
        return hist.loc[target_dates[0], "Close"]

    results = {"ticker": ticker, "call_date": call_date, "base_price": base_price}
    for horizon in [1, 5, 30]:
        future_price = price_n_days_later(horizon)
        if future_price is not None:
            results[f"return_{horizon}d"] = (future_price - base_price) / base_price
        else:
            results[f"return_{horizon}d"] = None

    return results


def build_returns_dataset(transcript_log: list) -> pd.DataFrame:
    """
    Takes a list of {"ticker": ..., "call_date": ...} dicts and returns
    a DataFrame with forward returns for each.
    """
    rows = []
    for entry in transcript_log:
        try:
            r = get_forward_returns(entry["ticker"], entry["call_date"])
            r["quarter"] = entry.get("quarter")
            rows.append(r)
        except Exception as e:
            print(f"Skipped {entry['ticker']} {entry.get('call_date')}: {e}")
    return pd.DataFrame(rows)


if __name__ == "__main__":
    # quick smoke test
    print(get_forward_returns("TGT", "2025-05-21"))
