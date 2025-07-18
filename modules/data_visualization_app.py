import streamlit as st
import pandas as pd

from modules.data_loader import load_data
from modules.state_manager import initialize_session_state, merge_settings, load_user_settings, load_config
from modules.ui_components import file_uploader, graph_type_selector, add_setting_buttons
from modules.filters import filter_dataframe
from modules.plot import create_plot, create_fft_plot
from modules.utils import download_chart_html
from modules.data_processing import rotate_xy, calc_accel_metrics, compute_fft
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

# 目的選択肢のリスト（将来的に追加予定）
purpose_options = ["加速度"]

def app():
    # セッション状態にリセットフラグを追加し、存在しない場合はデフォルトでFalseを設定
    if 'reset_triggered' not in st.session_state:
        st.session_state['reset_triggered'] = False
    
    # Initialize default FFT-related settings if they don't exist
    if 'fft_toggle' not in st.session_state:
        st.session_state['fft_toggle'] = False
    if 'fft_sample_size' not in st.session_state:
        st.session_state['fft_sample_size'] = 256
    if 'fft_start_sec' not in st.session_state:
        st.session_state['fft_start_sec'] = 0.0

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

            # 目的を指定するトグル
            specify_purpose = st.toggle(
                "目的を指定する",
                value=st.session_state.get("specify_purpose", False),
                key="specify_purpose_toggle",
            )
            st.session_state["specify_purpose"] = specify_purpose

            # 目的の選択
            if specify_purpose:
                selected_purpose = st.selectbox(
                    "目的を選択",
                    purpose_options,
                    key="purpose_selectbox",
                )
                st.session_state["selected_purpose"] = selected_purpose

                if selected_purpose == "加速度":
                    accel_cols = st.columns(3)
                    with accel_cols[0]:
                        x_col = st.selectbox("x軸", df.columns, key="accel_x_col")
                    with accel_cols[1]:
                        y_col = st.selectbox("y軸", df.columns, key="accel_y_col")
                    with accel_cols[2]:
                        z_col = st.selectbox("z軸", df.columns, key="accel_z_col")

                    angle = st.slider(
                        "XY平面回転角度(CCW+)",
                        min_value=-90.0,
                        max_value=90.0,
                        value=0.0,
                        step=1.0,
                        key="accel_angle",
                    )

                    rot_df = rotate_xy(df, x_col, y_col, angle)
                    time_series = None
                    for t_col in ["経過時間(sec)", "time(sec)"]:
                        if t_col in df.columns:
                            time_series = df[t_col].astype(float)
                            break

                    accel_df = pd.DataFrame(
                        {
                            "X": rot_df["x_rot"],
                            "Y": rot_df["y_rot"],
                            "Z": df[z_col].astype(float),
                        }
                    )
                    if time_series is not None:
                        accel_df["Time"] = time_series

                    st.session_state["accel_df"] = accel_df

                    with st.expander("変換後データ"):
                        st.dataframe(accel_df)
                        for axis_name in ["X", "Y", "Z"]:
                            metrics = calc_accel_metrics(accel_df[axis_name])
                            st.write(
                                f"**{axis_name}軸** 実効値: {metrics['rms']:.5g}, \
最大値: {metrics['max']:.5g}, 最小値: {metrics['min']:.5g}, \
peak to peak: {metrics['p2p']:.5g}"
                            )
            
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

                if st.session_state.get("selected_purpose") == "加速度":
                    fft_toggle = st.toggle(
                        "FFTを実施", value=st.session_state.get("fft_toggle", False), key="fft_toggle"
                    )

                    if fft_toggle:
                        sample_options = [2 ** i for i in range(6, 13)]
                        sample_size = st.select_slider(
                            "計算するサンプリング数",
                            options=sample_options,
                            value=st.session_state.get("fft_sample_size", 256),
                            key="fft_sample_size_slider",
                        )
                        st.session_state["fft_sample_size"] = sample_size

                        accel_df = st.session_state.get("accel_df")
                        if accel_df is not None:
                            interval = 1.0
                            for c in ["Time", "経過時間(sec)", "time(sec)"]:
                                if c in accel_df.columns and len(accel_df[c]) > 1:
                                    interval = float(accel_df[c].iloc[1]) - float(accel_df[c].iloc[0])
                                    break

                            max_start = max(0.0, (len(accel_df) - sample_size) * interval)
                            start_sec = st.slider(
                                "FFT開始位置(秒)",
                                min_value=0.0,
                                max_value=float(max_start),
                                value=st.session_state.get("fft_start_sec", 0.0),
                                step=interval,
                                key="fft_start_sec_slider",
                            )
                            st.session_state["fft_start_sec"] = start_sec

                            freqs, amp_df, interval = compute_fft(accel_df[[col for col in ["X", "Y", "Z", "Time"] if col in accel_df.columns]], start_sec, sample_size)
                            if len(freqs) > 0:
                                fft_fig = create_fft_plot(freqs, amp_df[[col for col in amp_df.columns if col != "Time"]])
                                st.plotly_chart(fft_fig)
                                st.write(f"Sampling interval inferred as {interval} seconds.")

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

