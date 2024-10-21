# modules/ui_components.py
import streamlit as st

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
