import pandas as pd
import numpy as np

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

