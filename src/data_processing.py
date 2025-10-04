import yfinance as yf
import pandas as pd
from pathlib import Path

# Base data directory (project_root/data)
DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Separate raw and processed directories
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Make sure they exist
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def fetch_stock_data(ticker, period="1y", interval="1d"):
    """
    Fetch historical stock data from Yahoo Finance and save raw CSV.
    Output format: Date,Open,High,Low,Close,Adj Close,Volume,Ticker
    """
    print(f"⬇Fetching {ticker} data...")
    stock = yf.download(ticker, period=period, interval=interval)

    if stock.empty:
        print(f"No data found for {ticker}.")
        return None

    # Reset index so Date becomes a column
    stock = stock.reset_index()

    # Add ticker column
    stock["Ticker"] = ticker

    # Save cleaned CSV
    file_path = RAW_DIR / f"{ticker}_data.csv"
    stock.to_csv(file_path, index=False)
    print(f"Raw data saved to {file_path}")
    return stock


if __name__ == "__main__":
    fetch_stock_data("AAPL")
