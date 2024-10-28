import streamlit as st
import pandas as pd
from modules.sample_data import load_simple_sample_data, load_timeseries_sample_data, load_histogram_sample_data, load_scatter_plot_sample_data, load_heatmap_sample_data
from modules.file_loader import load_csv_with_dynamic_start

def process_uploaded_file():
    uploaded_file = st.file_uploader("ファイルをアップロード", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df, measurement_interval, data_type = load_csv_with_dynamic_start(uploaded_file)
                st.write(f"{uploaded_file.name} をアップロードしました。")
                st.write(f"データの種類: {data_type}")
                st.write(f"測定間隔: {measurement_interval} 秒")
                return df
            elif uploaded_file.name.endswith('.xlsx'):
                return pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")
    return None

def load_sample_data():
    if st.button('サンプルデータを使用する。', key='button_sample'):
        use_sample_data = st.selectbox("サンプルデータの選択", ["単純データ", "時系列データ"])
        if use_sample_data == "単純データ":
            return load_simple_sample_data()
        elif use_sample_data == "時系列データ":
            return load_timeseries_sample_data()
    return None

def load_data(uploaded_file):
    """
    Load data from the uploaded file or provide sample data.
    
    Args:
        uploaded_file (file-like): The file uploaded by the user.

    Returns:
        pd.DataFrame or None: The loaded data as a DataFrame.
    """
    # ファイルアップロードが存在する場合
    if uploaded_file is not None:
        try:
            st.session_state['df_origin'] = None

            # CSVファイルの場合
            if uploaded_file.name.lower().endswith('.csv'):
                st.write(f"{uploaded_file.name} was uploaded.")
                st.session_state['df_origin'], measurement_interval, st.session_state['data_type'] = load_csv_with_dynamic_start(uploaded_file)
                st.write(f"Type of data is {st.session_state['data_type']}")
                st.write(f"Measurement interval is {measurement_interval} sec")

            # Excelファイルの場合
            elif uploaded_file.name.lower().endswith('.xlsx'):
                st.session_state['df_origin'] = pd.read_excel(uploaded_file)

        except Exception as e:
            st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")

    # サンプルデータを使用する場合
    else:
        # サンプルデータの選択状態を維持するために session_state を使用
        if 'sample_data_type' not in st.session_state:
            st.session_state['sample_data_type'] = "単純データ"

        use_sample_data = st.selectbox("サンプルデータの選択", ["単純データ", "時系列データ", "ヒストグラム用データ", "散布図用データ", "ヒートマップ用データ"], index=["単純データ", "時系列データ", "ヒストグラム用データ", "散布図用データ", "ヒートマップ用データ"].index(st.session_state['sample_data_type']), key='sample_data_selectbox')
        st.session_state['sample_data_type'] = use_sample_data

        # サンプルデータの生成
        if use_sample_data == "単純データ":
            st.session_state['df_origin'] = load_simple_sample_data()
        elif use_sample_data == "時系列データ":
            st.session_state['df_origin'] = load_timeseries_sample_data()
        elif use_sample_data == "ヒストグラム用データ":
            st.session_state['df_origin'] = load_histogram_sample_data()
        elif use_sample_data == "散布図用データ":
            st.session_state['df_origin'] = load_scatter_plot_sample_data()            
        elif use_sample_data == "ヒートマップ用データ":
            st.session_state['df_origin'] = load_heatmap_sample_data()
        
        st.write('Sample data is ' + use_sample_data)

    return st.session_state.get('df_origin', None)
