import logging
from pathlib import Path

import pandas as pd
import yfinance as yf

from config.settings import (
    DEFAULT_INTERVAL,
    DEFAULT_PERIOD,
    RAW_DATA_DIR,
    STOCKS,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def download_stock(
    ticker: str,
    period: str = "1y",
    interval: str = "1d",
    output_directory: Path = RAW_DATA_DIR
) -> pd.DataFrame:
    """
    Download historical stock data from Yahoo Finance
    and save it as a CSV file.

    Args:
        ticker (str): Stock ticker symbol.
        period (str): Historical data period.
        interval (str): Data interval.
        output_directory (Path): Directory to save CSV.

    Returns:
        pd.DataFrame: Downloaded stock data.
    """

    logging.info(f"Downloading stock data for {ticker}")

    try:
        df = yf.download(
            tickers=ticker,
            period=period,
            interval=interval,
            progress=False
        )

    except Exception as e:
        logging.error(f"Failed to download {ticker}: {e}")
        return pd.DataFrame()
    
    if df.empty:
        logging.warning(f"No data found for ticker: {ticker}")
        return df
    
    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        logging.info("Flattening MultiIndex columns")
        df.columns = [str(column) for column in df.columns.get_level_values(0)]
        
        df = df.reset_index()

    # Create a clean filename
    filename = (
        ticker.replace("^", "")
            .replace(".", "_")
            + ".csv"
    )

    output_path = output_directory / filename

    df.to_csv(output_path, index=False)

    logging.info(f"Data saved successfully: {output_path}")

    return df

def main():
    for ticker in STOCKS:
        download_stock(
            ticker=ticker,
            period=DEFAULT_PERIOD,
            interval=DEFAULT_INTERVAL,
            output_directory=RAW_DATA_DIR
        )

if __name__ == "__main__":
    main()