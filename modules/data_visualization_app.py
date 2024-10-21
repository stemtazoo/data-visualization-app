import json
import os

import streamlit as st
import pandas as pd

from modules.state_manager import initialize_session_state
from modules.ui_components import file_uploader, graph_type_selector
from modules.sample_data import load_simple_sample_data, load_timeseries_sample_data
from modules.file_loader import load_csv_with_dynamic_start
from modules.filters import filter_dataframe
from modules.plot import create_plot
from modules.utils import download_chart_html

# 設定ファイルの読み込み
def load_config(config_file_path='config/config.json'):
    with open(config_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ユーザー設定の読み込み
def load_user_settings(user_settings_file='config/user_settings.json'):
    if os.path.exists(user_settings_file):
        with open(user_settings_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {}

# ユーザー設定の保存
def save_user_settings(settings, user_settings_file='config/user_settings.json'):
    with open(user_settings_file, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)
        st.success("設定が保存されました！")

config = load_config()
user_settings = load_user_settings()

def app():
    # 状態を初期化（ユーザー設定を反映）
    initial_state = config['default_settings']
    initial_state.update(user_settings)
    initialize_session_state(initial_state)

    # タイトルの表示
    st.title(config['default_settings']['title'])

    # タブの作成
    tab_titles = config['default_settings']['tab_titles']
    tab1, tab2 = st.tabs(tab_titles)

    with tab1:
        # ファイルアップロードのインターフェース
        uploaded_file = file_uploader()
        
        if uploaded_file is not None:
            try:
                st.session_state['df_origin'] = None
                
                if uploaded_file.name.lower().endswith('.csv'):
                    st.write(uploaded_file.name + ' was uploaded.')
                    st.session_state['df_origin'], measurement_interval, st.session_state['data_type'] = load_csv_with_dynamic_start(uploaded_file)
                    st.write('Type of data is ' + st.session_state['data_type'])
                    st.write(f'Measurement interval is {measurement_interval} sec')
                    
                elif uploaded_file.name.endswith('.xlsx'):
                    st.session_state['df_origin'] = pd.read_excel(uploaded_file)
                    
            except Exception as e:
                st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")
        else:
            # サンプルデータの生成ボタン
            use_sample_data = st.selectbox("サンプルデータの選択", ["単純データ", "時系列データ"])
            if use_sample_data == "単純データ":
                st.session_state['df_origin'] = load_simple_sample_data()
            elif use_sample_data == "時系列データ":
                st.session_state['df_origin'] = load_timeseries_sample_data()

        if st.session_state['df_origin'] is not None:
            # フィルタの適用
            df = filter_dataframe(st.session_state['df_origin'])
            
            # データプレビュー
            with st.expander("データプレビュー"):
                st.dataframe(df)

            # グラフの種類を選択
            chart_type = graph_type_selector(st.session_state['data_type'])

            # チェックボックス
            customize_title = st.checkbox("グラフのタイトルと軸をカスタマイズする", value=st.session_state['customize_title'], key="customize_title_checkbox")

            x_axis = st.selectbox("X軸を選択", df.columns, key="x_axis_selectbox")
            
            y_axis = []
            if st.session_state['data_type'] == 'GRAPHTEC':
                y_axis = st.multiselect("Y軸を選択", df.columns, df.columns.to_list()[3:-3], key="y_axis_selectbox")
            elif st.session_state['data_type'] == 'NR600':
                y_axis = st.multiselect("Y軸を選択", df.columns, df.columns.to_list()[1:], key="y_axis_selectbox")
            else:
                y_axis = st.multiselect("Y軸を選択", df.columns, key="y_axis_selectbox")

            # 折れ線グラフの場合、第2軸の設定を追加
            use_secondary_y = False
            secondary_y_axis = []
            primary_y_axis = []
            if chart_type == "折れ線グラフ":
                use_secondary_y = st.checkbox("第2軸（右側Y軸）を使用する", key="use_secondary_y_checkbox")
                if use_secondary_y:
                    primary_y_axis = st.multiselect("第1軸（左側Y軸）を選択", y_axis, key="primary_y_axis_multiselect")
                    secondary_y_axis = st.multiselect("第2軸（右側Y軸）を選択", [col for col in y_axis if col not in primary_y_axis], key="secondary_y_axis_multiselect")
                else:
                    primary_y_axis = y_axis
            else:
                primary_y_axis = y_axis

            if customize_title:
                customize_graph_title = st.checkbox("グラフのタイトルをカスタマイズする", value=(st.session_state['graph_title'] != ''), key="customize_graph_title_checkbox")
                if customize_graph_title:
                    st.session_state['graph_title'] = st.text_input("グラフのタイトル", value=st.session_state['graph_title'], key="graph_title_input")
                    st.session_state['title_font_size'] = st.slider("グラフのタイトルのサイズ", 10, 40, st.session_state['title_font_size'], key="title_font_size_slider")
                else:
                    st.session_state['graph_title'] = ''

                # X軸タイトルのカスタマイズ
                customize_x_axis_title = st.checkbox("X軸のタイトルをカスタマイズする", value=(st.session_state['x_axis_title'] != x_axis), key="customize_x_axis_title_checkbox")
                if customize_x_axis_title:
                    st.session_state['x_axis_title'] = st.text_input("X軸のタイトル", value=st.session_state['x_axis_title'], key="x_axis_title_input")
                else:
                    st.session_state['x_axis_title'] = x_axis

                # Y軸タイトルのカスタマイズ
                customize_y_axis_title = st.checkbox("Y軸のタイトルをカスタマイズする", value=(st.session_state['y_axis_title'] != y_axis), key="customize_y_axis_title_checkbox")
                if customize_y_axis_title:
                    st.session_state['y_axis_title'] = st.text_input("第1軸（左側Y軸）のタイトル", value=st.session_state['y_axis_title'], key="y_axis_title_input")
                    if use_secondary_y:
                        st.session_state['secondary_y_axis_title'] = st.text_input("第2軸（右側Y軸）のタイトル", value=st.session_state.get('secondary_y_axis_title', ''), key="secondary_y_axis_title_input")
                else:
                    st.session_state['y_axis_title'] = ', '.join(primary_y_axis)
                    if use_secondary_y:
                        st.session_state['secondary_y_axis_title'] = ', '.join(secondary_y_axis)

                st.session_state['x_axis_title_font_size'] = st.slider("X軸のタイトルのサイズ", 10, 30, st.session_state['x_axis_title_font_size'], key="x_axis_title_font_size_slider")
                st.session_state['y_axis_title_font_size'] = st.slider("Y軸のタイトルのサイズ", 10, 30, st.session_state['y_axis_title_font_size'], key="y_axis_title_font_size_slider")
                st.session_state['x_axis_value_size'] = st.slider("X軸の値のサイズ", 10, 30, st.session_state['x_axis_value_size'], key="x_axis_value_size_slider")
                st.session_state['y_axis_value_size'] = st.slider("Y軸の値のサイズ", 10, 30, st.session_state['y_axis_value_size'], key="y_axis_value_size_slider")
            else:
                st.session_state['graph_title'] = ''
                st.session_state['x_axis_title'] = x_axis
                st.session_state['y_axis_title'] = ', '.join(primary_y_axis)
                if use_secondary_y:
                    st.session_state['secondary_y_axis_title'] = ', '.join(secondary_y_axis)

            st.session_state['customize_title'] = customize_title

            # 設定を保存する辞書
            settings = {
                'x_axis': x_axis,
                'y_axis': primary_y_axis,
                'secondary_y_axis': secondary_y_axis,
                'use_secondary_y': use_secondary_y,  # この部分を追加
                'graph_title': st.session_state['graph_title'],
                'title_font_size': st.session_state['title_font_size'],
                'x_axis_title': st.session_state['x_axis_title'],
                'y_axis_title': st.session_state['y_axis_title'],
                'secondary_y_axis_title': st.session_state.get('secondary_y_axis_title', ''),
                'x_axis_title_font_size': st.session_state['x_axis_title_font_size'],
                'y_axis_title_font_size': st.session_state['y_axis_title_font_size'],
                'x_axis_value_size': st.session_state['x_axis_value_size'],
                'y_axis_value_size': st.session_state['y_axis_value_size']
            }

            # 設定の保存ボタン
            if st.button("設定を保存"):
                save_user_settings(settings)

            fig, graph_title = create_plot(chart_type, df, settings)
            if fig:
                st.plotly_chart(fig)
                download_chart_html(fig, graph_title)

            # ダウンロードリンクの提供
            st.download_button("Download CSV", data=df.to_csv(index=False), file_name='processed_data.csv')

    with tab2:
        st.header("データ可視化アプリの使い方")
        st.markdown("""
        このアプリでは、以下の手順でデータの可視化を行います。

        1. **ファイルのアップロード**:
            - CSV または Excel ファイルをアップロードします。
        2. **サンプルデータの使用**:
            - サンプルデータ（単純データまたは時系列データ）を使用することもできます。
        3. **データのフィルタリング**:
            - `Add filters` チェックボックスを有効にすると、特定の列でデータをフィルタリングできます。
        4. **グラフの選択**:
            - グラフの種類を選択し、X軸とY軸の列を指定します。
            - 折れ線グラフでは第1軸と第2軸（右側Y軸）を指定することができます。
            - 必要に応じて、色分けのための列を指定します。
        5. **グラフのカスタマイズ**:
            - `グラフのタイトルと軸をカスタマイズする` チェックボックスを有効にすると、グラフのタイトル、X軸とY軸のタイトル、タイトルのフォントサイズ、およびX軸とY軸の値のフォントサイズをカスタマイズできます。
        6. **ユーザー設定の保存**:
            - カスタマイズした設定を保存することができます。保存した設定は次回起動時に再利用されます。
        7. **グラフの表示とダウンロード**:
            - グラフが表示され、`Download Chart` ボタンをクリックすると、HTMLファイルとしてグラフをダウンロードできます。
            - `Download CSV` ボタンをクリックすると、フィルタリングされたデータをCSVファイルとしてダウンロードできます。

        ### 注意事項
        - 大きなデータセットの場合、フィルタリングやグラフの描画に時間がかかることがあります。
        - ファイルのアップロードは、ローカル環境でのみ動作します。
        """)


