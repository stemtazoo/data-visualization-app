# modules/ui_components.py
import streamlit as st

from modules.state_manager import reset_session_state_to_default, apply_user_settings, save_user_settings

def file_uploader():
    return st.file_uploader("ファイルをアップロード", type=["csv", "xlsx"])

def graph_type_selector(data_type):
    if data_type == 'GRAPHTEC':
        chart_types = ["折れ線グラフ"]
    elif data_type == 'NR600':
        chart_types = ["折れ線グラフ"]
    else:
        chart_types = ["折れ線グラフ", "棒グラフ", "ヒストグラム", "散布図", "ヒートマップ"]
    return st.selectbox("グラフの種類を選択", chart_types, key="chart_type_selectbox")

def add_setting_buttons(config, user_settings):
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("ユーザー設定を保存", key='button_save'):
            save_user_settings(st.session_state['graph_settings'])

    with col2:
        if st.button("デフォルト設定を読み込み", key='button_reset'):
            reset_session_state_to_default(config)
            st.rerun()

    with col3:
        if st.button("ユーザー設定を再読み込み", key='button_reload'):
            apply_user_settings(user_settings)
            st.rerun()