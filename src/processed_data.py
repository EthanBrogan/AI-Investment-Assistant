import pandas as pd
from pathlib import Path

# Base data directory (project_root/data)
DATA_DIR = Path(__file__).resolve().parents[1] / "data"

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def process_stock_data(ticker: str):
    """
    Load raw stock data for a given ticker,
    clean it, and save to processed folder.
    """
    raw_path = RAW_DIR / f"{ticker}_data.csv"
    processed_path = PROCESSED_DIR / f"{ticker}_processed.csv"

    if not raw_path.exists():
        print(
            f"Raw file not found for {ticker}. Did you run data_collection.py?")
        return

    # Load raw data
    df = pd.read_csv(raw_path, parse_dates=["Date"], index_col="Date")

    # Example cleaning: drop NA, sort by date
    df = df.dropna().sort_index()

    # Pick the right price column
    price_col = "Adj Close" if "Adj Close" in df.columns else "Close"

    # Example feature: daily returns
    df["Daily_Return"] = df[price_col].pct_change()

    # Save processed data
    df.to_csv(processed_path)
    print(f"Processed data saved to {processed_path}")


if __name__ == "__main__":
    process_stock_data("AAPL")
