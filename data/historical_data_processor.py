import pandas as pd
import yfinance as yf

class DataProcessor:
    @staticmethod
    def data(symbol: str, date_start: str, date_end: str) -> pd.DataFrame:
        """
        Fetch historical data for a given symbol between date_start and date_end.

        Args:
            symbol (str): Ticker symbol (e.g., 'SPY').
            date_start (str): Start date in 'YYYY-MM-DD' format.
            date_end (str): End date in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: Historical OHLCV data.
        """
        df = yf.download(symbol, start=date_start, end=date_end)
        return df

# Example usage:
# processor = DataProcessor()
# df = processor.data("SPY", "2023-01-01", "2023-12-31")
# print(df.head())