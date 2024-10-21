import pandas as pd
import numpy as np

# サンプルデータの生成
def load_sample_data():
    data = {
        'X軸': [1, 2, 3, 4, 5],
        'Y軸': [10, 20, 30, 40, 50],
        'Z軸': [5, 4, 3, 2, 1]
    }
    return pd.DataFrame(data)

def load_simple_sample_data():
    data = {
        'X軸': [1, 2, 3, 4, 5],
        'Y軸': [10, 20, 30, 40, 50],
        'Z軸': [5, 4, 3, 2, 1]
    }
    return pd.DataFrame(data)

def load_timeseries_sample_data():
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    data = {
        '日付': dates,
        '値': np.random.randn(100).cumsum()
    }
    return pd.DataFrame(data)