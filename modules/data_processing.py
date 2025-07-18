import pandas as pd
import numpy as np
import streamlit as st

def preprocess_data(df):
    # データの前処理をここに記述
    df = df.dropna()  # 例: 欠損値の削除
    return df


def rotate_xy(df: pd.DataFrame, x_col: str, y_col: str, angle_deg: float) -> pd.DataFrame:
    """Rotate X and Y columns by the given angle.

    Parameters
    ----------
    df : pd.DataFrame
        Source dataframe containing X and Y columns.
    x_col, y_col : str
        Column names corresponding to X and Y axes.
    angle_deg : float
        Rotation angle in degrees. Positive is counter-clockwise.

    Returns
    -------
    pd.DataFrame
        DataFrame with two columns ``x_rot`` and ``y_rot`` containing the rotated values.
    """
    angle_rad = np.deg2rad(angle_deg)
    x = df[x_col].astype(float)
    y = df[y_col].astype(float)
    x_rot = x * np.cos(angle_rad) - y * np.sin(angle_rad)
    y_rot = x * np.sin(angle_rad) + y * np.cos(angle_rad)
    return pd.DataFrame({"x_rot": x_rot, "y_rot": y_rot})


def calc_accel_metrics(series: pd.Series) -> dict:
    """Calculate acceleration metrics for a numeric series.

    Returns a dictionary with RMS, max, min and peak-to-peak values.
    """
    values = series.astype(float)
    rms = np.sqrt(np.mean(values ** 2))
    max_val = values.max()
    min_val = values.min()
    p2p = max_val - min_val
    return {
        "rms": rms,
        "max": max_val,
        "min": min_val,
        "p2p": p2p,
    }


def _infer_sampling_interval(df: pd.DataFrame) -> float:
    """Infer sampling interval from known time columns."""
    for col in ["Time", "経過時間(sec)", "time(sec)"]:
        if col in df.columns and len(df[col]) > 1:
            try:
                return float(df[col].iloc[1]) - float(df[col].iloc[0])
            except Exception:
                continue
    return 1.0


def compute_fft(df: pd.DataFrame, start_sec: float, sample_size: int):
    """Compute FFT for acceleration dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing at least acceleration columns (e.g. ``X``, ``Y``, ``Z``)
        and optionally a time column.
    start_sec : float
        Start time in seconds for FFT calculation.
    sample_size : int
        Number of samples to use for FFT. Should be a power of two.

    Returns
    -------
    tuple
        ``(freqs, amp_df)`` where ``freqs`` is a numpy array of frequency bins and
        ``amp_df`` is a DataFrame containing amplitude spectra for each column.
    """

    interval = _infer_sampling_interval(df)
    start_index = int(start_sec / interval)
    end_index = start_index + sample_size
    if end_index > len(df):
        end_index = len(df)
        start_index = max(0, end_index - sample_size)
    segment = df.iloc[start_index:end_index]
    n = len(segment)
    if n == 0:
        return np.array([]), pd.DataFrame()

    data_values = segment.select_dtypes(include=[float, int]).values
    # サンプル数で正規化を行う。
    fft_vals = np.fft.rfft(data_values, axis=0)
    freqs = np.fft.rfftfreq(n, d=interval)
    
    # 振幅スペクトルの計算
    amplitude = np.abs(fft_vals) * 2 / n  # 2/n で正規化
    amplitude[0] = amplitude[0] / 2       # DC成分は元に戻す
    
    # ナイキスト成分の処理（サンプル数が偶数の場合）
    if n % 2 == 0:
        amplitude[-1] = amplitude[-1] / 2
    
    amp_df = pd.DataFrame(amplitude, columns=segment.select_dtypes(include=[float, int]).columns)
    return freqs, amp_df, interval


def compute_fft_segments(df: pd.DataFrame, sample_size: int):
    """Compute FFT repeatedly over segments of ``sample_size``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing numeric columns to transform. A ``Time`` column is
        optional for inferring the sampling interval.
    sample_size : int
        Number of samples per FFT segment.

    Returns
    -------
    tuple
        ``(freqs, times, spec_dict, interval)`` where ``freqs`` is an array of
        frequency bins, ``times`` is an array of segment start times, and
        ``spec_dict`` maps column names to 2-D amplitude arrays of shape
        ``(len(freqs), len(times))``.
    """

    interval = _infer_sampling_interval(df)
    n_segments = len(df) // sample_size
    if n_segments == 0:
        return np.array([]), np.array([]), {}, interval

    freqs = np.fft.rfftfreq(sample_size, d=interval)
    times = np.arange(n_segments) * sample_size * interval

    spec_dict = {}
    numeric_cols = df.select_dtypes(include=[float, int]).columns
    for col in numeric_cols:
        spectra = []
        for i in range(n_segments):
            seg = df[col].iloc[i * sample_size : (i + 1) * sample_size].astype(float).values
            fft_vals = np.fft.rfft(seg)
            amplitude = np.abs(fft_vals) * 2 / sample_size
            amplitude[0] /= 2
            if sample_size % 2 == 0:
                amplitude[-1] /= 2
            spectra.append(amplitude)
        spec_dict[col] = np.column_stack(spectra)

    return freqs, times, spec_dict, interval

