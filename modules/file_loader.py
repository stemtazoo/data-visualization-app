import re

import pandas as pd

def extract_measurement_interval(lines):
    """
    Extract the measurement interval from the raw CSV lines.

    Args:
    lines (list): List of lines from the CSV file.

    Returns:
    float: The measurement interval in seconds.
    """
    for line in lines:
        if line.strip().startswith("測定間隔"):
            match = re.search(r"測定間隔\s*,\s*(\d+)s", line)
            if match:
                interval_s = float(match.group(1))
                return interval_s

def load_csv_with_dynamic_start(upload_file, encodings=['utf-8', 'cp932']):
    """
    Reads a CSV file and returns a pandas DataFrame.
    
    The function dynamically detects the header and data start line. It looks for the row where the first column
    contains the word "測定値" and treats it as the header. The data starts from the second line after the header.
    
    Args:
    upload_file (None): streamlit file uploader.
    encoding (str): The encoding of the CSV file.
    
    Returns:
    pd.DataFrame: A DataFrame containing the data from the CSV file.
    """
    
    # read csv file
    for encoding in encodings:
        try:
            lines = [line.decode(encoding) for line in upload_file]
            break
        except:
            pass
    
    # ヘッダー行を見つける（1列目が「測定値」となる行を探す）
    for i, line in enumerate(lines):
        if line.strip().startswith("測定値"):
            header_line = i + 1
            # データの種類
            data_type = 'GRAPHTEC'
            break
        if line.strip().startswith("#EndHeader"):
            header_line = i
            # データの種類
            data_type = 'NR600'
            break
        else:
            # データの種類
            data_type = 'None'
    
    if data_type == 'GRAPHTEC':
        # 測定間隔を抽出
        measurement_interval = extract_measurement_interval(lines)
        
        # データの開始行を設定（ヘッダー行の2行後）
        data_start_line = header_line + 2
        
        # ヘッダーを抽出
        header = lines[header_line].strip().split(',')
        
        # streamlitの問題に対処。列名が同じだったらエラーになるのを回避
        # 置換する文字列
        replacement = "replace"
        
        # 空白を任意の文字列に置換
        header = [replacement + str(i) if x.strip() == "" else x for i, x in enumerate(header)]
        
        # データを抽出
        data_lines = lines[data_start_line:]
        data = [line.strip().split(',') for line in data_lines]
        
        # DataFrameを作成
        df = pd.DataFrame(data, columns=header)
        
        # 経過時間を追加
        df['経過時間(sec)'] = df.index.astype('float') * measurement_interval
    elif data_type == 'NR600':
        # データの開始行を設定
        data_start_line = header_line + 1

        # データの最終行を設定
        # ヘッダー行を見つける（1列目が「測定値」となる行を探す）
        for i, line in enumerate(lines):
            if line.strip().startswith("#BeginMark"):
                data_end_line = i - 1
                break
        
        # ヘッダーを抽出
        header = lines[header_line].strip().split(',')
        
        # streamlitの問題に対処。列名が同じだったらエラーになるのを回避
        # 置換する文字列
        replacement = "replace"
        
        # 空白を任意の文字列に置換
        header = [replacement + str(i) if x.strip() == "" else x for i, x in enumerate(header)]
        
        # データを抽出
        data_lines = lines[data_start_line:data_end_line]
        data = [line.strip().split(',') for line in data_lines]
        
        # DataFrameを作成
        df = pd.DataFrame(data, columns=header)
        
        # columns rename
        df = df.rename(columns={'#EndHeader': 'time(sec)'})
        
        # measurement interval (sec)
        df['日時(μs)'] = df['日時(μs)'].astype(float)
        measurement_interval = (df.at[1, '日時(μs)'] - df.at[0, '日時(μs)']) / 1000000
        
        # time
        df['time(sec)'] = df.index * measurement_interval
        
        # 不要な行削除
        del df['日時(μs)']
        
    else:
        measurement_interval = None
        df =  pd.read_csv(upload_file)
    
    return df, measurement_interval, data_type
