import streamlit as st
import pandas as pd

from modules.data_loader import load_data
from modules.state_manager import initialize_session_state, merge_settings, load_user_settings, load_config
from modules.ui_components import file_uploader, graph_type_selector, add_setting_buttons
from modules.filters import filter_dataframe
from modules.plot import create_plot
from modules.utils import download_chart_html
from modules.ui_customizer import customize_chart_settings
from modules.help_content import render_help_tab

config = load_config()
user_settings = load_user_settings()

# グラフタイプと設定ファイル内のキーをマッピングする辞書
chart_type_mapping = {
    "折れ線グラフ": "line_chart",
    "棒グラフ": "bar_chart",
    "散布図": "scatter_plot",
    "ヒートマップ": "heatmap",
    "ヒストグラム": "histogram"
}

def app():
    # セッション状態にリセットフラグを追加し、存在しない場合はデフォルトでFalseを設定
    if 'reset_triggered' not in st.session_state:
        st.session_state['reset_triggered'] = False

    # 初期設定の読み込みと初期化
    if not st.session_state['reset_triggered']:
        initial_state = merge_settings(config['default_settings'], user_settings)
        initialize_session_state(initial_state)
        st.session_state['reset_triggered'] = True

    # タイトルの表示
    st.title(st.session_state['title'])

    # タブの作成
    tab_titles = st.session_state['tab_titles']
    tab1, tab2, tab3 = st.tabs(tab_titles)

    with tab1:
        # データのロード
        df = load_data(file_uploader())

        if df is not None:
            # filter
            df = filter_dataframe(df)  
            
            # see data
            with st.expander('See data!'):
                st.dataframe(df)
            
            # グラフの種類を選択
            chart_type = graph_type_selector(st.session_state['data_type'])

            # グラフ設定の読み込み
            chart_key = chart_type_mapping.get(chart_type, "default_settings")

            # X軸の選択
            if chart_type == 'ヒートマップ':
                x_axis = st.selectbox("X軸を選択", ['column'], key="x_axis_selectbox")
            else:
                x_axis = st.selectbox("X軸を選択", st.session_state['df_origin'].columns, key="x_axis_selectbox")
            
            st.session_state['graph_settings'][chart_key]['x_axis'] = x_axis

            # Y軸の選択
            y_axis = []
            if st.session_state['data_type'] == 'GRAPHTEC':
                y_axis = st.multiselect("Y軸を選択", st.session_state['df_origin'].columns, st.session_state['df_origin'].columns.to_list()[3:-3], key="y_axis_selectbox")
            elif st.session_state['data_type'] == 'NR600':
                y_axis = st.multiselect("Y軸を選択", st.session_state['df_origin'].columns, st.session_state['df_origin'].columns.to_list()[1:], key="y_axis_selectbox")
            elif chart_type == 'ヒートマップ':
                y_axis_list = ['dataframe index', st.session_state['df_origin'].columns[0]]
                y_axis = st.selectbox("Y軸を選択", y_axis_list, key="y_axis_selectbox")
                if y_axis != 'dataframe index':
                    st.session_state['df_origin'] = st.session_state['df_origin'].set_index(y_axis)
            else:
                y_axis = st.multiselect("Y軸を選択", st.session_state['df_origin'].columns, key="y_axis_selectbox")
            
            st.session_state['graph_settings'][chart_key]['y_axis'] = y_axis

            # 折れ線グラフの場合、第2軸の設定を追加
            use_secondary_y = False
            if chart_type == '折れ線グラフ':
                use_secondary_y = st.checkbox("第2軸（右側Y軸）を使用する", key="use_secondary_y_checkbox", value=st.session_state.get('use_secondary_y', False))

            if use_secondary_y:
                st.session_state['graph_settings'][chart_key]['use_secondary_y'] = use_secondary_y  # session_state に反映

                # y_axisの中からのみデフォルト値を選択する
                primary_y_axis_default = [value for value in st.session_state.get('primary_y_axis', []) if value in y_axis]

                primary_y_axis = st.multiselect(
                    "第1軸（左側Y軸）を選択",
                    y_axis,
                    default=primary_y_axis_default,
                    key="primary_y_axis_multiselect"
                )
                st.session_state['graph_settings'][chart_key]['primary_y_axis'] = primary_y_axis  # session_state に反映
                
                # y_axisの中からのみデフォルト値を選択する
                secondary_y_axis_default = [value for value in st.session_state.get('secondary_y_axis', []) if value in y_axis]

                secondary_y_axis = st.multiselect(
                    "第2軸（右側Y軸）を選択",
                    [col for col in y_axis if col not in primary_y_axis],
                    default=secondary_y_axis_default,
                    key="secondary_y_axis_multiselect"
                )
                st.session_state['graph_settings'][chart_key]['secondary_y_axis'] = secondary_y_axis  # session_state に反映
            else:
                primary_y_axis = y_axis
                secondary_y_axis = st.session_state.get('secondary_y_axis', [])
                st.session_state['graph_settings'][chart_key]['use_secondary_y'] = use_secondary_y  # session_state に反映
                st.session_state['graph_settings'][chart_key]['primary_y_axis'] = primary_y_axis  # session_state に反映

            # グラフのカスタマイズ
            customize_title = st.checkbox("グラフのタイトルと軸をカスタマイズする", value=st.session_state['customize_title'], key="customize_title_checkbox")
            if customize_title:
                customize_chart_settings(chart_key)
            else:
                if chart_type == '折れ線グラフ':
                    if st.session_state['graph_settings'][chart_key]['x_axis_title'] == '':
                        st.session_state['graph_settings'][chart_key]['x_axis_title'] = ", ".join(st.session_state['graph_settings'][chart_key]['x_axis'])
                    
                    if st.session_state['graph_settings'][chart_key]['y_axis_title'] == '':
                        st.session_state['graph_settings'][chart_key]['y_axis_title'] = ", ".join(st.session_state['graph_settings'][chart_key]['y_axis'])

            # グラフの作成と表示
            fig, graph_title = create_plot(chart_type, st.session_state['df_origin'], st.session_state['graph_settings'][chart_key])
            if fig:
                st.plotly_chart(fig)
                download_chart_html(fig, graph_title)

            # ダウンロードリンクの提供
            st.download_button("Download CSV", data=st.session_state['df_origin'].to_csv(index=False), file_name='processed_data.csv')
            
            # 設定ボタンの追加
            add_setting_buttons(config, user_settings)

    with tab2:
        render_help_tab()

    with tab3:
        with st.expander('session state'):
            st.write(st.session_state)

        with st.expander('config'):
            st.write(config)

        with st.expander('user settings'):
            st.write(user_settings)

