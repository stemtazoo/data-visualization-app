import streamlit as st

def customize_graph_settings(df, settings):
    """
    Customize graph settings including title, axis labels, font sizes, and secondary y-axis.

    Args:
    df (pd.DataFrame): DataFrame for the graph.
    settings (dict): The configuration settings for the graph.
    """

    # グラフのタイトルと軸のカスタマイズを有効化するかどうか
    customize_title = st.checkbox("グラフのタイトルと軸をカスタマイズする", value=settings.get('customize_title', False), key="customize_title_checkbox")

    if customize_title:
        # グラフタイトルのカスタマイズ
        st.subheader("グラフのタイトル設定")
        customize_graph_title = st.checkbox("グラフのタイトルをカスタマイズする", value=settings.get('graph_title', '') != '', key="customize_graph_title_checkbox")
        if customize_graph_title:
            settings['graph_title'] = st.text_input("グラフのタイトル", value=settings.get('graph_title', ''), key="graph_title_input")
            settings['title_font_size'] = st.slider("グラフのタイトルのサイズ", 10, 40, settings.get('title_font_size', 20), key="title_font_size_slider")
        else:
            settings['graph_title'] = ''

        # X軸の設定
        st.subheader("X軸の設定")
        settings['x_axis_title'] = configure_axis_settings(df, "X軸", "x_axis_title", False, settings)

        # Y軸の設定
        st.subheader("Y軸の設定")
        settings['y_axis_title'] = configure_axis_settings(df, "Y軸", "y_axis_title", False, settings)

        # 二次Y軸の設定
        use_secondary_y = st.checkbox("第2軸（右側Y軸）を使用する", value=settings.get('use_secondary_y', False), key="use_secondary_y_checkbox")
        settings['use_secondary_y'] = use_secondary_y

        if use_secondary_y:
            st.subheader("第2軸（右側Y軸）の設定")
            settings['secondary_y_axis_title'] = configure_axis_settings(df, "第2軸（右側Y軸）", "secondary_y_axis_title", True, settings)

        # フォントサイズの設定
        st.subheader("フォントサイズ設定")
        settings['x_axis_title_font_size'] = st.slider("X軸のタイトルのサイズ", 10, 30, settings.get('x_axis_title_font_size', 12), key="x_axis_title_font_size_slider")
        settings['y_axis_title_font_size'] = st.slider("Y軸のタイトルのサイズ", 10, 30, settings.get('y_axis_title_font_size', 12), key="y_axis_title_font_size_slider")
        settings['x_axis_value_size'] = st.slider("X軸の値のサイズ", 10, 30, settings.get('x_axis_value_size', 12), key="x_axis_value_size_slider")
        settings['y_axis_value_size'] = st.slider("Y軸の値のサイズ", 10, 30, settings.get('y_axis_value_size', 12), key="y_axis_value_size_slider")

    return settings


def configure_axis_settings(df, axis_name, axis_key, is_secondary, settings):
    """
    Configure axis settings such as title for X or Y axis.

    Args:
    df (pd.DataFrame): DataFrame for the graph.
    axis_name (str): Name of the axis (e.g., 'X軸', 'Y軸').
    axis_key (str): Key for accessing axis title in the settings.
    is_secondary (bool): Whether this axis is secondary or not.
    settings (dict): The configuration settings for the graph.

    Returns:
    str: The axis title after customization.
    """
    customize_axis_title = st.checkbox(f"{axis_name}のタイトルをカスタマイズする", value=(settings.get(axis_key, '') != ''), key=f"customize_{axis_key}_checkbox")
    if customize_axis_title:
        axis_title = st.text_input(f"{axis_name}のタイトル", value=settings.get(axis_key, ''), key=f"{axis_key}_input")
    else:
        # デフォルトはカスタマイズしない場合、DataFrameの列名から自動設定
        if not is_secondary:
            axis_title = st.selectbox(f"{axis_name}を選択", df.columns, key=f"{axis_key}_selectbox")
        else:
            axis_title = settings.get(axis_key, '')
    
    return axis_title

def customize_chart_settings(chart_key):
    customize_graph_title = st.checkbox("グラフのタイトルをカスタマイズする", value=(st.session_state['graph_settings'][chart_key]['graph_title'] != ''), key="customize_graph_title_checkbox")
    if customize_graph_title:
        st.session_state['graph_settings'][chart_key]['graph_title'] = st.text_input("グラフのタイトル", value=st.session_state['graph_settings'][chart_key]['graph_title'], key="graph_title_input")
        st.session_state['graph_settings'][chart_key]['title_font_size'] = st.slider("グラフのタイトルのサイズ", 10, 40, st.session_state['graph_settings'][chart_key]['title_font_size'], key="title_font_size_slider")

    # X軸タイトルのカスタマイズ
    customize_x_axis_title = st.checkbox("X軸のタイトルをカスタマイズする", value=(st.session_state['graph_settings'][chart_key]['x_axis_title'] != st.session_state['graph_settings'][chart_key]['x_axis']), key="customize_x_axis_title_checkbox")
    if customize_x_axis_title:
        st.session_state['graph_settings'][chart_key]['x_axis_title'] = st.text_input("X軸のタイトル", value=st.session_state['graph_settings'][chart_key]['x_axis_title'], key="x_axis_title_input")

    # Y軸タイトルのカスタマイズ
    customize_y_axis_title = st.checkbox("Y軸のタイトルをカスタマイズする", value=(st.session_state['graph_settings'][chart_key]['y_axis_title'] != st.session_state['graph_settings'][chart_key]['y_axis']), key="customize_y_axis_title_checkbox")
    if customize_y_axis_title:
        st.session_state['graph_settings'][chart_key]['y_axis_title'] = st.text_input("第1軸（左側Y軸）のタイトル", value=st.session_state.get('y_axis_title', ''), key="y_axis_title_input")
        if st.session_state['graph_settings'][chart_key]['use_secondary_y']:
            st.session_state['graph_settings'][chart_key]['secondary_y_axis_title'] = st.text_input("第2軸（右側Y軸）のタイトル", value=st.session_state.get('secondary_y_axis_title', ''), key="secondary_y_axis_title_input")
    else:
        st.session_state['graph_settings'][chart_key]['y_axis_title'] = ', '.join(st.session_state['graph_settings'][chart_key]['primary_y_axis'])
        if st.session_state['graph_settings'][chart_key]['use_secondary_y']:
            st.session_state['graph_settings'][chart_key]['secondary_y_axis_title'] = ', '.join(st.session_state['graph_settings'][chart_key]['secondary_y_axis'])

    st.session_state['graph_settings'][chart_key]['x_axis_title_font_size'] = st.slider("X軸のタイトルのサイズ", 10, 30, st.session_state['graph_settings'][chart_key]['x_axis_title_font_size'], key="x_axis_title_font_size_slider")
    st.session_state['graph_settings'][chart_key]['y_axis_title_font_size'] = st.slider("Y軸のタイトルのサイズ", 10, 30, st.session_state['graph_settings'][chart_key]['y_axis_title_font_size'], key="y_axis_title_font_size_slider")
    st.session_state['graph_settings'][chart_key]['x_axis_value_size'] = st.slider("X軸の値のサイズ", 10, 30, st.session_state['graph_settings'][chart_key]['x_axis_value_size'], key="x_axis_value_size_slider")
    st.session_state['graph_settings'][chart_key]['y_axis_value_size'] = st.slider("Y軸の値のサイズ", 10, 30, st.session_state['graph_settings'][chart_key]['y_axis_value_size'], key="y_axis_value_size_slider")

