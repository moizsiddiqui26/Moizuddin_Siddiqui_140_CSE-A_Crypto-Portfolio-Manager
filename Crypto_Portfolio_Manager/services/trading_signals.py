import pandas as pd
import numpy as np

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate the Relative Strength Index (RSI).
    """
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    # Calculate Smoothed moving average
    for i in range(period, len(series)):
        avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * (period - 1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * (period - 1) + loss.iloc[i]) / period

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_moving_averages(series: pd.Series, short_window=7, long_window=21):
    """
    Calculate short and long window moving averages.
    """
    short_ma = series.rolling(window=short_window, min_periods=1).mean()
    long_ma = series.rolling(window=long_window, min_periods=1).mean()
    return short_ma, long_ma


def generate_buy_sell_signals(df: pd.DataFrame) -> dict:
    """
    Analyzes existing price data and returns an actionable signal and explanation.
    Returns: { "signal": "STRONG BUY", "reason": "...", "rsi": 30.5, ... }
    """
    if df.empty or len(df) < 21:
        return {"signal": "HOLD", "reason": "Not enough data for meaningful analysis.", "rsi": 50, "trend": "Neutral"}

    close_prices = df["Close"]
    
    rsi = calculate_rsi(close_prices).iloc[-1]
    short_ma, long_ma = calculate_moving_averages(close_prices)
    
    cur_short = short_ma.iloc[-1]
    cur_long = long_ma.iloc[-1]
    prev_short = short_ma.iloc[-2]
    prev_long = long_ma.iloc[-2]
    
    # Defaults
    signal = "HOLD"
    reason = "Market is relatively stable, hold positions to mitigate risk."
    trend = "Neutral"

    # Analyze Trend (MA crossover)
    is_golden_cross = cur_short > cur_long and prev_short <= prev_long
    is_death_cross = cur_short < cur_long and prev_short >= prev_long
    trend_up = cur_short > cur_long
    
    if trend_up:
        trend = "Bullish (Upward)"
    else:
        trend = "Bearish (Downward)"

    # Determine RSI limits
    # Usually < 30 is oversold (good buy), > 70 is overbought (good sell)
    # But since Crypto is volatile, we adjust lightly.
    
    if rsi < 30 and trend_up:
        signal = "STRONG BUY"
        reason = "Coin is historically heavily undervalued (oversold) AND starting an upward trend!"
    elif rsi < 35 or is_golden_cross:
        signal = "BUY"
        reason = "Good buying opportunity. Positive momentum starting."
    elif rsi > 70 and not trend_up:
        signal = "STRONG SELL"
        reason = "Coin is historically overvalued (overbought) AND starting a downward trend. Take profits!"
    elif rsi > 65 or is_death_cross:
        signal = "SELL"
        reason = "Coin might be peaking. Good time to consider taking some profits."
    
    return {
        "signal": signal,
        "reason": reason,
        "rsi": round(rsi if not pd.isna(rsi) else 50.0, 2),
        "trend": trend
    }
