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

# ヒストグラム用のサンプルデータを生成
def load_histogram_sample_data():
    np.random.seed(42)
    data = {
        'Value': np.random.normal(0, 1, 1000)  # 平均0、標準偏差1の正規分布からサンプルを生成
    }
    return pd.DataFrame(data)

# 散布図用のサンプルデータを生成
def load_scatter_plot_sample_data():
    np.random.seed(42)
    data = {
        'X': np.random.rand(100),  # 0から1の一様分布からサンプルを生成
        'Y': np.random.rand(100),
        'Category': np.random.choice(['A', 'B', 'C'], size=100)  # ランダムなカテゴリ
    }
    return pd.DataFrame(data)

# ヒートマップ用のサンプルデータを生成
def load_heatmap_sample_data():
    np.random.seed(42)
    data = np.random.rand(10, 10)  # 10x10のランダムなデータを生成
    df = pd.DataFrame(data, columns=[f'Column {i+1}' for i in range(10)], index=[f'Row {i+1}' for i in range(10)])
    return df