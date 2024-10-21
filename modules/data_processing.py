import pandas as pd

def preprocess_data(df):
    # データの前処理をここに記述
    df = df.dropna()  # 例: 欠損値の削除
    return df
