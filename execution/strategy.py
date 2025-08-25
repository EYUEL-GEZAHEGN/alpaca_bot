import pandas as pd
from data.live_data_processor import DataProcessor

class Strategy:
    """Simple moving average crossover strategy."""

    def __init__(self, short_window: int = 5, long_window: int = 20):
        self.short_window = short_window
        self.long_window = long_window
        self.dp = DataProcessor()

    def generate_signal(self) -> dict:
        """Generate trading signal based on moving average crossover.

        Returns:
            dict: Contains 'signal' (buy/sell/hold), 'reason', and 'price'.
        """
        df = self.dp.get_recent_data()
        if df is None or len(df) < self.long_window:
            return {"signal": "hold", "reason": "Not enough data", "price": None}

        df["short_ma"] = df["close"].rolling(window=self.short_window).mean()
        df["long_ma"] = df["close"].rolling(window=self.long_window).mean()

        price = df["close"].iloc[-1]
        short_prev, long_prev = df["short_ma"].iloc[-2], df["long_ma"].iloc[-2]
        short_curr, long_curr = df["short_ma"].iloc[-1], df["long_ma"].iloc[-1]

        if short_prev <= long_prev and short_curr > long_curr:
            return {
                "signal": "buy",
                "reason": "Short MA crossed above long MA",
                "price": price,
            }
        if short_prev >= long_prev and short_curr < long_curr:
            return {
                "signal": "sell",
                "reason": "Short MA crossed below long MA",
                "price": price,
            }
        return {"signal": "hold", "reason": "No crossover", "price": price}

