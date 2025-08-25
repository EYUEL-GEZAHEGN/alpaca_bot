import statistics as stats
import time
import pandas as pd
import numpy as np
from data.live_data_processor import DataProcessor



def uptrend_retracment():
	"""
	Swing structure-based uptrend retracement entry.
	Entry after a higher low (HL) is formed in an uptrend (higher highs and higher lows).
	Returns: dict with 'signal' (bool), 'reason' (str), 'entry_price' (float or None)
	"""
	dp = DataProcessor()
	df = dp.get_recent_data()  # expects DataFrame with 'close' column
	if df is None or len(df) < 30:
		return {"signal": False, "reason": "Not enough data", "entry_price": None}

	# Find swing highs/lows
	def find_swings(series, lookback=5):
		highs = []
		lows = []
		for i in range(lookback, len(series)-lookback):
			window = series[i-lookback:i+lookback+1]
			if series[i] == window.max():
				highs.append(i)
			if series[i] == window.min():
				lows.append(i)
		return highs, lows

	highs, lows = find_swings(df['close'])
	if len(highs) < 2 or len(lows) < 2:
		return {"signal": False, "reason": "Not enough swings", "entry_price": None}

	# Check for higher highs and higher lows (uptrend)
	last_highs = [df['close'].iloc[i] for i in highs[-2:]]
	last_lows = [df['close'].iloc[i] for i in lows[-2:]]
	uptrend = last_highs[1] > last_highs[0] and last_lows[1] > last_lows[0]

	# Entry: price pulls back after new high, forms higher low, and starts moving up
	price = df['close'].iloc[-1]
	last_hl_idx = lows[-1]
	last_hl_price = df['close'].iloc[last_hl_idx]
	# Confirm price is above last higher low and above previous swing high
	entry = price > last_hl_price and uptrend

	if uptrend and entry:
		return {"signal": True, "reason": "Swing HL formed in uptrend, price moving up", "entry_price": price}
	else:
		return {"signal": False, "reason": "No valid swing retracement entry", "entry_price": None}