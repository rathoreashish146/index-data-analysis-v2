"""
Utility functions for data processing, calculations, and analysis.
"""

import base64
import io
import numpy as np
import pandas as pd
from dash import html, dash_table


def parse_csv_flexible(contents: str, filename: str):
    """
    Accept TWO columns: one date/time-like and one numeric (names can be anything).
    Detect them and normalize to ['datetime','index'].
    """
    if not filename or not filename.lower().endswith(".csv"):
        return None, [], f"Please upload a CSV file. You uploaded: {filename}"

    try:
        _, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df0 = pd.read_csv(io.BytesIO(decoded))
    except Exception as e:
        return None, [], f"Failed to read CSV: {e}"

    if df0.empty:
        return None, [], "The CSV appears to be empty."
    if df0.shape[1] < 2:
        return None, [], "CSV must have at least two columns (a date column and a numeric column)."

    warnings = []

    # Find date-like column (≥50% parseable)
    date_col = None
    for c in df0.columns:
        s = pd.to_datetime(df0[c], errors="coerce", infer_datetime_format=True)
        if s.notna().mean() >= 0.5:
            date_col = c
            break
    if date_col is None:
        return None, [], "Could not detect a date column."

    # Find numeric column (≥50% numeric)
    num_col = None
    for c in df0.columns:
        if c == date_col:
            continue
        s = pd.to_numeric(df0[c], errors="coerce")
        if s.notna().mean() >= 0.5:
            num_col = c
            break
    if num_col is None:
        return None, [], "Could not detect a numeric column."

    df = pd.DataFrame({
        "datetime": pd.to_datetime(df0[date_col], errors="coerce"),
        "index": pd.to_numeric(df0[num_col], errors="coerce")
    })
    before = len(df)
    df = df.dropna(subset=["datetime", "index"]).sort_values("datetime").reset_index(drop=True)
    dropped = before - len(df)
    if dropped > 0:
        warnings.append(f"Dropped {dropped} rows with invalid/missing values.")
    return df, warnings, None


def compute_range(preset: str, start_date, end_date, data_min: pd.Timestamp, data_max: pd.Timestamp, snap_month: bool):
    """
    Resolve (start, end) timestamps based on a preset or DatePickerRange values.
    """
    start, end = data_min, data_max

    if preset in (None, "all"):
        start, end = data_min, data_max
    elif preset == "ytd":
        end = data_max
        start = pd.Timestamp(end.year, 1, 1)
    elif preset == "1y":
        end = data_max
        start = end - pd.DateOffset(years=1)
    elif preset == "3y":
        end = data_max
        start = end - pd.DateOffset(years=3)
    elif preset == "6m":
        end = data_max
        start = end - pd.DateOffset(months=6)
    else:  # "custom"
        s = pd.to_datetime(start_date) if start_date else data_min
        e = pd.to_datetime(end_date) if end_date else data_max
        start, end = s, e

    if snap_month:
        start = pd.Timestamp(start.year, start.month, 1)
        end = (pd.Timestamp(end.year, end.month, 1) + pd.offsets.MonthEnd(1)).normalize()

    start = max(start, data_min)
    end = min(end, data_max)
    if start > end:
        start, end = end, start
    return start, end


def end_trade_day_with_buffer(start: pd.Timestamp, window_size_days: int,
                              buffer_minus: int = 1, buffer_plus: int = 1) -> pd.Timestamp:
    """
    Weekend-aware last trading day for a calendar-day window.
    - Tentative end = start + (window_size_days - 1) calendar days.
    - If tentative lands on weekend:
        - If the backward adjustment would skip more than one day (e.g., Sat→Fri = -1 is OK,
          Sun→Fri = -2 means instead take +1 and go forward to Monday).
    """
    if pd.isna(start):
        return pd.NaT

    start = (start if isinstance(start, pd.Timestamp) else pd.Timestamp(start)).normalize()
    tentative = start + pd.Timedelta(days=max(int(window_size_days) - 1, 0))

    weekday = tentative.weekday()  # Monday=0 … Sunday=6
    # Saturday → -1 to Friday
    if weekday == 5:
        return tentative - pd.Timedelta(days=buffer_minus)
    # Sunday → instead of -2 back to Friday, go +1 to Monday
    elif weekday == 6:
        return tentative + pd.Timedelta(days=buffer_plus)
    # Weekday
    return tentative


def compute_windowed_returns_calendar(df: pd.DataFrame, window_size_days: int) -> pd.Series:
    """
    Compute % change using a calendar-day window with weekend-aware snapping.
    Assumes df has columns ['datetime','index'] and is sorted by datetime.
    For each row i at date D_i, find E_i = end_trade_day_with_buffer(D_i, window_size_days).
    Use the latest available row with datetime <= E_i as end value.
    
    Special case: window_size_days=1 uses backward-looking pct_change (today/yesterday - 1).
    """
    if df.empty:
        return pd.Series(dtype=float)

    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"]).dt.normalize()
    df = df.dropna(subset=["datetime", "index"]).sort_values("datetime").reset_index(drop=True)

    ws = max(int(window_size_days or 1), 1)
    vals = pd.to_numeric(df["index"], errors="coerce")
    
    # Special handling for 1-day returns: use backward-looking pct_change
    # This computes (today / yesterday) - 1, which is the standard daily return
    if ws == 1:
        rets = vals.pct_change(1).values
        return pd.Series(rets, index=df.index, name="ret_1d_cal")

    dates = df["datetime"]

    # Map unique day -> last row pos
    date_to_lastpos = {}
    for pos, day in enumerate(dates):
        date_to_lastpos[day] = pos
    unique_days = dates.drop_duplicates().reset_index(drop=True)

    def pos_leq_day(target_day: pd.Timestamp):
        # rightmost unique_days[idx] <= target_day
        left, right = 0, len(unique_days) - 1
        ans = -1
        while left <= right:
            mid = (left + right) // 2
            if unique_days[mid] <= target_day:
                ans = mid
                left = mid + 1
            else:
                right = mid - 1
        if ans == -1:
            return None
        return date_to_lastpos[unique_days[ans]]

    rets = np.full(len(df), np.nan, dtype=float)
    vals_arr = vals.values

    for i in range(len(df)):
        start_day = dates.iloc[i]
        end_day = end_trade_day_with_buffer(start_day, ws)
        j = pos_leq_day(end_day)
        if j is None or j <= i:
            continue
        if np.isfinite(vals_arr[i]) and np.isfinite(vals_arr[j]) and vals_arr[i] != 0:
            rets[i] = (vals_arr[j] / vals_arr[i]) - 1.0

    return pd.Series(rets, index=df.index, name=f"ret_{ws}d_cal")


def ema(s: pd.Series, span: int):
    """Exponential Moving Average"""
    return s.ewm(span=span, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14):
    """Relative Strength Index"""
    delta = series.diff()
    up = (delta.clip(lower=0)).rolling(period).mean()
    down = (-delta.clip(upper=0)).rolling(period).mean()
    rs = up / (down.replace(0, np.nan))
    out = 100 - (100 / (1 + rs))
    return out


def bbands_mid_upper_lower(price: pd.Series, window: int = 20, k: float = 2.0):
    """Bollinger Bands"""
    mid = price.rolling(window).mean()
    std = price.rolling(window).std()
    upper = mid + k * std
    lower = mid - k * std
    return mid, upper, lower


def compute_calendar_return_series(df: pd.DataFrame, window_size_days: int) -> pd.Series:
    """
    Wrapper that returns weekend-aware calendar returns aligned to df.index,
    using compute_windowed_returns_calendar.
    """
    return compute_windowed_returns_calendar(df[["datetime","index"]].copy(), window_size_days)


def build_indicators(df: pd.DataFrame, price_col="index"):
    """
    Builds a feature table.
    Weekend-aware for ret_5, ret_10, mom_10 via compute_windowed_returns_calendar.
    Other rolling features operate on available trading days.
    """
    out = pd.DataFrame(index=df.index)
    p = pd.to_numeric(df[price_col], errors="coerce").astype(float)

    # returns, momentum & volatility
    out["ret_1"]  = p.pct_change(1)

    # weekend-aware multi-day returns
    out["ret_5"]  = compute_calendar_return_series(df, 5)
    out["ret_10"] = compute_calendar_return_series(df, 10)
    # momentum over 10 calendar days == ret_10
    out["mom_10"] = out["ret_10"]

    # volatility based on daily returns (trading-day based)
    out["vol_20"] = out["ret_1"].rolling(20).std()
    out["vol_60"] = out["ret_1"].rolling(60).std()

    # moving averages
    out["sma_5"]   = p.rolling(5).mean()
    out["sma_20"]  = p.rolling(20).mean()
    out["ema_12"]  = ema(p, 12)
    out["ema_26"]  = ema(p, 26)

    # MACD family
    macd_line = out["ema_12"] - out["ema_26"]
    macd_sig  = ema(macd_line, 9)
    out["macd"]      = macd_line
    out["macd_sig"]  = macd_sig
    out["macd_hist"] = macd_line - macd_sig

    # RSI
    out["rsi_14"] = rsi(p, 14)

    # Bollinger
    mid, up, lo = bbands_mid_upper_lower(p, 20, 2.0)
    out["bb_mid"]   = mid
    out["bb_up"]    = up
    out["bb_lo"]    = lo
    out["bb_width"] = (up - lo) / mid
    out["bb_pos"]   = (p - mid) / (up - lo)

    # drawdown features
    rolling_max = p.cummax()
    drawdown = p / rolling_max - 1.0
    out["dd"]       = drawdown
    out["dd_20"]    = (p / p.rolling(20).max() - 1.0)
    out["dd_speed"] = drawdown.diff()

    # combos
    out["sma_gap_5_20"]  = out["sma_5"] / out["sma_20"] - 1.0
    out["ema_gap_12_26"] = out["ema_12"] / out["ema_26"] - 1.0

    return out


def drop_event_analysis(df: pd.DataFrame, minimum_per_drop: float, windows_size: int):
    """
    Count drop events using weekend-aware windowed returns.
    """
    ret = compute_windowed_returns_calendar(df, windows_size)
    ret = ret.dropna()
    crossings = (ret <= -minimum_per_drop)
    total_events = int(crossings.sum())
    denom = max(len(ret), 1)
    prob = total_events / denom
    key = f"{windows_size} days and {minimum_per_drop * 100:.0f}% minimum percentage drop"
    return {key: {"events": total_events, "probability": f"{prob:.2%}"}}


def gain_event_analysis(df: pd.DataFrame, minimum_per_gain: float, windows_size: int):
    """
    Count gain events using weekend-aware windowed returns.
    """
    ret = compute_windowed_returns_calendar(df, windows_size)
    ret = ret.dropna()
    crossings = (ret >= minimum_per_gain)
    total_events = int(crossings.sum())
    denom = max(len(ret), 1)
    prob = total_events / denom
    key = f"{windows_size} days and {minimum_per_gain * 100:.0f}% minimum percentage gain"
    return {key: {"events": total_events, "probability": f"{prob:.2%}"}}


def build_trade_window_table(df: pd.DataFrame, window_size_days: int, limit: int = 200):
    """
    Table of start date, weekend-aware last trade day, and actual end present in data (<= last trade day).
    """
    if df.empty:
        return html.Div()

    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"]).dt.normalize()
    df = df.dropna(subset=["datetime", "index"]).sort_values("datetime").reset_index(drop=True)

    dates = df["datetime"]

    # Map unique days to last position
    date_to_lastpos = {}
    for pos, day in enumerate(dates):
        date_to_lastpos[day] = pos
    unique_days = dates.drop_duplicates().reset_index(drop=True)

    def pos_leq_day(target_day: pd.Timestamp):
        left, right = 0, len(unique_days) - 1
        ans = -1
        while left <= right:
            mid = (left + right) // 2
            if unique_days[mid] <= target_day:
                ans = mid
                left = mid + 1
            else:
                right = mid - 1
        if ans == -1:
            return None
        return date_to_lastpos[unique_days[ans]]

    ws = max(int(window_size_days or 1), 1)
    rows = []
    for i in range(len(df)):
        start_day = dates.iloc[i]
        last_trade_day = end_trade_day_with_buffer(start_day, ws)
        j = pos_leq_day(last_trade_day)
        actual_end = dates.iloc[j] if (j is not None and j > i) else pd.NaT
        rows.append({
            "Start (first day of trade)": start_day.date(),
            "Last day of trade (weekend-aware)": last_trade_day.date() if pd.notna(last_trade_day) else None,
            "Actual end in data (<= last trade day)": actual_end.date() if pd.notna(actual_end) else None,
        })

    df_out = pd.DataFrame(rows)
    if limit and len(df_out) > limit:
        df_out = df_out.head(limit)

    table = dash_table.DataTable(
        data=df_out.to_dict("records"),
        columns=[{"name": c, "id": c} for c in df_out.columns],
        page_size=min(20, len(df_out)) or 5,
        page_action="native",
        page_current=0,
        style_table={"overflowX": "auto", "backgroundColor": "#1a1a1a"},
        style_cell={
            "textAlign": "left", 
            "minWidth": "160px",
            "backgroundColor": "#1a1a1a",
            "color": "rgba(255,255,255,0.9)",
            "border": "1px solid rgba(255,255,255,0.1)",
            "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
        },
        style_header={
            "backgroundColor": "#252525",
            "color": "rgba(255,255,255,0.95)",
            "fontWeight": "600",
            "border": "1px solid rgba(0,200,150,0.3)",
            "textAlign": "left"
        },
        style_data={
            "backgroundColor": "#1a1a1a",
            "color": "rgba(255,255,255,0.9)",
            "border": "1px solid rgba(255,255,255,0.1)"
        },
        style_data_conditional=[
            {
                "if": {"row_index": "even"},
                "backgroundColor": "#222222",
            },
            {
                "if": {"state": "selected"},
                "backgroundColor": "rgba(0,200,150,0.2)",
                "border": "1px solid rgba(0,200,150,0.5)"
            }
        ],
        style_cell_conditional=[
            {
                "if": {"column_id": "Start (first day of trade)"},
                "minWidth": "180px"
            }
        ]
    )
    return table


def compute_drawdown_recovery(
    df: pd.DataFrame,
    date_col: str = "datetime",
    price_col: str = "index",
    recovery_mode: str = "prior_high",
):
    """
    Compute drawdown episodes and days-to-recovery for a price series.
    
    Parameters
    ----------
    df : pd.DataFrame
        Must contain `date_col` (date-like) and `price_col` (float).
    date_col : str
        Column with dates.
    price_col : str
        Column with price / index level.
    recovery_mode : {'prior_high', 'new_high_or_equal'}
        - 'prior_high'          : recover when price >= *that episode's* peak value
        - 'new_high_or_equal'   : same as prior_high (alias, kept for clarity)
    
    Returns
    -------
    events_df : pd.DataFrame
        Columns:
            peak_date, peak_value,
            trough_date, trough_value,
            recovery_date, recovery_value,
            drawdown_pct, days_to_trough, days_to_recovery
        (Open drawdowns with no recovery will have NA recovery fields.)
    annotated : pd.DataFrame
        Original series plus:
            cum_max, drawdown, drawdown_pct
    """
    # Ensure columns exist
    if date_col not in df.columns:
        raise ValueError(f"Column '{date_col}' not found in dataframe. Available columns: {list(df.columns)}")
    if price_col not in df.columns:
        raise ValueError(f"Column '{price_col}' not found in dataframe. Available columns: {list(df.columns)}")
    
    data = df[[date_col, price_col]].copy()
    data[date_col] = pd.to_datetime(data[date_col], errors='coerce')
    data = data.dropna(subset=[date_col, price_col])
    data[price_col] = pd.to_numeric(data[price_col], errors='coerce')
    data = data.dropna(subset=[price_col])
    data = data.sort_values(date_col).reset_index(drop=True)
    
    if data.empty:
        return pd.DataFrame(), pd.DataFrame()
    
    # Running peak & drawdown
    data["cum_max"] = data[price_col].cummax()
    data["drawdown"] = data[price_col] - data["cum_max"]
    data["drawdown_pct"] = data["drawdown"] / data["cum_max"]
    
    dates = data[date_col].to_list()
    prices = data[price_col].to_list()
    n = len(data)
    
    episodes = []
    i = 0
    
    # Advance to first record high (start of first episode)
    while i < n and (i == 0 or prices[i] < data.loc[i, "cum_max"]):
        if i == 0 and prices[i] == max(prices[: i + 1]):
            break
        i += 1
    
    # Scan peak -> trough -> recovery
    while i < n:
        peak_idx = i
        peak_val = prices[peak_idx]
        peak_date = dates[peak_idx]
        
        # Move forward until recovery (price >= peak_val) or series ends.
        j = peak_idx + 1
        trough_idx = peak_idx
        trough_val = peak_val
        
        while j < n and prices[j] < peak_val:
            if prices[j] < trough_val:
                trough_val = prices[j]
                trough_idx = j
            j += 1
        
        trough_date = dates[trough_idx]
        dd_pct = (trough_val - peak_val) / peak_val
        days_to_trough = trough_idx - peak_idx
        
        if j < n and prices[j] >= peak_val:
            # Recovered
            recovery_idx = j
            recovery_val = prices[recovery_idx]
            recovery_date = dates[recovery_idx]
            days_to_recovery = recovery_idx - peak_idx
            
            episodes.append({
                "peak_date": peak_date,
                "peak_value": float(peak_val),
                "trough_date": trough_date,
                "trough_value": float(trough_val),
                "recovery_date": recovery_date,
                "recovery_value": float(recovery_val),
                "drawdown_pct": float(dd_pct),     # negative number (e.g. -0.20)
                "days_to_trough": int(days_to_trough),
                "days_to_recovery": int(days_to_recovery),
            })
            
            # Start next episode at this recovery point's next *record* high
            i = recovery_idx + 1
            # fast-forward to next record high (start of next episode)
            while i < n and prices[i] < max(prices[: i + 1]):
                i += 1
        else:
            # No recovery by end of data → open drawdown
            episodes.append({
                "peak_date": peak_date,
                "peak_value": float(peak_val),
                "trough_date": trough_date,
                "trough_value": float(trough_val),
                "recovery_date": pd.NaT,
                "recovery_value": pd.NA,
                "drawdown_pct": float(dd_pct),
                "days_to_trough": int(days_to_trough),
                "days_to_recovery": pd.NA,
            })
            break
    
    events_df = pd.DataFrame(episodes)
    annotated = data.copy()
    
    return events_df, annotated

