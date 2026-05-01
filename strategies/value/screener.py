"""
Value Investing Screener
Filters stocks based on classic value metrics.
"""

import argparse
import yfinance as yf
import pandas as pd

# Default watchlist (aligned with user's interests)
DEFAULT_WATCHLIST = {
    "HK": ["0700.HK", "3968.HK", "0005.HK"],
    "US": ["JPM", "PG", "PEP", "KO", "JPM", "PG", "PEP"]
}

def screen_stock(ticker: str) -> dict:
    """Screen a single stock."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.fast_info
        hist = stock.history(period="1d")

        if not hist.empty:
            price = hist["Close"].iloc[-1]
        else:
            price = info.get("last_price", 0)

        return {
            "ticker": ticker,
            "price": price,
            "pe_ratio": info.get("pe_ratio", None),
            "pb_ratio": info.get("price_book_ratio", None),
            "dividend_yield": info.get("dividend_yield", 0) * 100 if info.get("dividend_yield") else 0,
            "market_cap": info.get("market_cap", 0),
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def screen_watchlist(tickers: list, max_pe: float = 15, max_pb: float = 1.5, min_div: float = 3.0) -> pd.DataFrame:
    """Screen a list of tickers."""
    results = []
    for t in tickers:
        data = screen_stock(t)
        if "error" not in data:
            results.append(data)

    df = pd.DataFrame(results)

    # Apply value filters
    if not df.empty:
        df = df[
            (df["pe_ratio"] < max_pe) &
            (df["pb_ratio"] < max_pb) &
            (df["dividend_yield"] > min_div)
        ]

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Value Investing Screener")
    parser.add_argument("--market", choices=["hk", "us"], default="us")
    parser.add_argument("--max_pe", type=float, default=15)
    parser.add_argument("--max_pb", type=float, default=1.5)
    parser.add_argument("--min_div", type=float, default=3.0)
    args = parser.parse_args()

    tickers = DEFAULT_WATCHLIST.get("HK" if args.market == "hk" else "US", [])
    results = screen_watchlist(tickers, args.max_pe, args.max_pb, args.min_div)

    if results.empty:
        print("No stocks match your value criteria.")
    else:
        print(results.to_string(index=False))
