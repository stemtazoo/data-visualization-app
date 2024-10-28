import re
import pandas as pd
import streamlit as st

header_cache = {'header_line': None, 'data_type': None}  # ヘッダー行とデータタイプのキャッシュ

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
            match = re.search(r"測定間隔\s*,\s*(\d+(?:\.\d+)?)s", line)
            if match:
                interval_s = float(match.group(1))
                return interval_s
    return None

def load_csv_with_dynamic_start(upload_file, encodings=['utf-8', 'cp932', 'shift_jis']):
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
    lines = None
    for encoding in encodings:
        try:
            upload_file.seek(0)  # ファイルポインタを先頭にリセット
            lines = [line.decode(encoding) for line in upload_file]
            break
        except UnicodeDecodeError:
            continue
    
    if lines is None:
        raise ValueError("ファイルの読み込みに失敗しました。対応するエンコーディングが見つかりませんでした。")


    # データタイプを見つける
    header_line = None
    data_type = None
    for i, line in enumerate(lines):
        if line.strip().startswith("測定値"):
            header_line = i + 1
            data_type = 'GRAPHTEC'
            break
        elif line.strip().startswith("#EndHeader"):
            header_line = i
            data_type = 'NR600'
            break
    
    # データタイプが不明な場合
    if data_type == None:
        global header_cache
        header_line = header_cache['header_line']
        data_type = header_cache['data_type']

        # キャッシュが有効な場合はそれを利用
        if header_line is not None and data_type is not None:
            st.info(f"前回の設定を使用しています: ヘッダー行 {header_line + 1}, データタイプ {data_type}")
        else:

            # GRAPHTECやNR600に当てはまらない場合、最初の文字列を含む行をheader_lineとするか確認
            while header_line is None:
                for i, line in enumerate(lines):
                    if line.strip():
                        if st.button(f"行 {i + 1} をヘッダーとして使用しますか？:\n{line.strip()}"):
                            header_line = i
                            if line.strip().startswith("index"):
                                data_type = 'headerあり'
                            else:
                                data_type = 'headerあり'
                            break
                        elif st.button("ヘッダーを見つけるのを続けますか？ それともヘッダーなしとしますか？"):
                            continue
                        else:
                            data_type = 'headerなし'
                            break
                if header_line is None and data_type == 'headerなし':
                    break
            
            # ヘッダー行が見つからない場合、処理を継続するか確認
            if header_line is None:
                if st.button("ヘッダーが見つかりませんでした。処理を継続しますか？"):
                    data_type = 'headerなし'
                else:
                    raise ValueError("ヘッダー行が見つかりませんでした。対応するフォーマットではない可能性があります。")
            
            # ヘッダー情報をキャッシュに保存
            header_cache['header_line'] = header_line
            header_cache['data_type'] = data_type
    
    if data_type == 'GRAPHTEC':
        # 測定間隔を抽出
        measurement_interval = extract_measurement_interval(lines)
        if measurement_interval is None:
            raise ValueError("測定間隔が見つかりませんでした。")
        
        # データの開始行を設定（ヘッダー行の2行後）
        data_start_line = header_line + 2
        
        # ヘッダーを抽出
        header = lines[header_line].strip().split(',')
        
        # streamlitの問題に対処。列名が同じだったらエラーになるのを回避
        replacement = "replace"
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
        data_end_line = len(lines)

        # データの最終行を設定
        for i, line in enumerate(lines[data_start_line:], start=data_start_line):
            if line.strip().startswith("#BeginMark"):
                data_end_line = i
                break
        
        # ヘッダーを抽出
        header = lines[header_line].strip().split(',')
        
        # streamlitの問題に対処。列名が同じだったらエラーになるのを回避
        replacement = "replace"
        header = [replacement + str(i) if x.strip() == "" else x for i, x in enumerate(header)]
        
        # データを抽出
        data_lines = lines[data_start_line:data_end_line]
        data = [line.strip().split(',') for line in data_lines]
        
        # DataFrameを作成
        df = pd.DataFrame(data, columns=header)
        
        # 列名のリネーム
        df = df.rename(columns={'#EndHeader': 'time(sec)'})
        
        # 日時(μs)をfloatに変換し、測定間隔を計算
        df['日時(μs)'] = df['日時(μs)'].astype(float)
        measurement_interval = (df.at[1, '日時(μs)'] - df.at[0, '日時(μs)']) / 1000000
        
        # 経過時間の追加
        df['time(sec)'] = df.index * measurement_interval
        
        # 不要な列を削除
        del df['日時(μs)']
    elif data_type == 'headerあり':
        # データの開始行を設定（ヘッダー行の1行後）
        data_start_line = header_line + 1
        
        # ヘッダーを抽出
        header = lines[header_line].strip().split(',')
        
        # streamlitの問題に対処。列名が同じだったらエラーになるのを回避
        replacement = "replace"
        header = [replacement + str(i) if x.strip() == "" else x for i, x in enumerate(header)]
        
        # データを抽出
        data_lines = lines[data_start_line:]
        data = [line.strip().split(',') for line in data_lines]
        
        # DataFrameを作成
        df = pd.DataFrame(data, columns=header)
        
        # 測定間隔は不明
        measurement_interval = None
    elif data_type == 'headerなし':
        # ヘッダーなしとしてデータを読み込む
        data_lines = lines
        data = [line.strip().split(',') for line in data_lines]
        
        # DataFrameを作成（ヘッダーなし）
        df = pd.DataFrame(data)
        
        # 測定間隔は不明
        measurement_interval = None
    else:
        # デフォルトの読み込み処理
        upload_file.seek(0)  # ファイルポインタを先頭にリセット
        df = pd.read_csv(upload_file, encoding=encodings[0])
        measurement_interval = None
    
    return df, measurement_interval, data_type
