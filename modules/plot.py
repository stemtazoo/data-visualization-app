import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# グラフ生成関数の定義
def create_plot(chart_type, df, settings):

    colors = px.colors.qualitative.Light24

    if chart_type in ["折れ線グラフ", "棒グラフ", "散布図"]:
        add_color = st.checkbox("凡例を追加する（color）", value=False)
        color = st.selectbox("凡例の列を選択", [None] + df.columns.tolist(), key="color_selectbox") if add_color else None

        if chart_type == "折れ線グラフ":
            if settings['use_secondary_y'] and settings['secondary_y_axis']:
                fig = go.Figure()
                for i, y in enumerate(settings['primary_y_axis']):
                    fig.add_trace(go.Scatter(x=df[settings['x_axis']], y=df[y], mode='lines', name=y, marker=dict(color=colors[i])))
                for j, y in enumerate(settings['secondary_y_axis']):
                    fig.add_trace(go.Scatter(x=df[settings['x_axis']], y=df[y], mode='lines', name=y, yaxis='y2', marker=dict(color=colors[i+j+1])))
                fig.update_layout(
                    yaxis2=dict(title=settings['secondary_y_axis_title'], overlaying='y', side='right'),
                    title={'text': settings['graph_title'], 'x': 0.5, 'xanchor': 'center', 'font': {'size': settings['title_font_size']}},
                    xaxis_title={'text': settings['x_axis_title'], 'font': {'size': settings['x_axis_title_font_size']}},
                    yaxis_title={'text': settings['y_axis_title'], 'font': {'size': settings['y_axis_title_font_size']}},
                    xaxis=dict(
                        tickfont=dict(size=settings['x_axis_value_size'])
                    ),
                    yaxis=dict(
                        tickfont=dict(size=settings['y_axis_value_size'])
                    )
                )
            else:
                fig = px.line(df, x=settings['x_axis'], y=settings['y_axis'], color=color, title=settings['graph_title'], color_discrete_sequence=colors)
        elif chart_type == "棒グラフ":
            fig = px.bar(df, x=settings['x_axis'], y=settings['y_axis'], color=color, title=settings['graph_title'], color_discrete_sequence=colors)
        elif chart_type == "散布図":
            fig = px.scatter(df, x=settings['x_axis'], y=settings['y_axis'], color=color, title=settings['graph_title'], color_discrete_sequence=colors)

        fig.update_layout(
            title={'text': settings['graph_title'], 'x': 0.5, 'xanchor': 'center', 'font': {'size': settings['title_font_size']}},
            xaxis_title={'text': settings['x_axis_title'], 'font': {'size': settings['x_axis_title_font_size']}},
            yaxis_title={'text': settings['y_axis_title'], 'font': {'size': settings['y_axis_title_font_size']}},
            xaxis=dict(
                tickfont=dict(size=settings['x_axis_value_size'])
            ),
            yaxis=dict(
                tickfont=dict(size=settings['y_axis_value_size'])
            )
        )
        return fig, settings['graph_title']

    elif chart_type == "ヒストグラム":
        numeric_columns = df.select_dtypes(include='number').columns.tolist()
        if not numeric_columns:
            st.warning("ヒストグラムを作成するには、数値列が必要です。")
            return None, None

        column = st.selectbox("列を選択", numeric_columns, key="histogram_column_selectbox")
        add_color = st.checkbox("凡例を追加する（color）", key="histogram_add_color_checkbox")
        color = st.selectbox("凡例の列を選択", [None] + df.columns.tolist(), key="histogram_color_selectbox") if add_color else None

        fig = px.histogram(df, x=column, color=color, title=settings['graph_title'], color_discrete_sequence=colors)
        fig.update_layout(
            title={'text': settings['graph_title'], 'x': 0.5, 'xanchor': 'center', 'font': {'size': settings['title_font_size']}},
            xaxis_title={'text': settings['x_axis_title'], 'font': {'size': settings['x_axis_title_font_size']}},
            yaxis_title={'text': settings['y_axis_title'], 'font': {'size': settings['y_axis_title_font_size']}},
            xaxis=dict(
                tickfont=dict(size=settings['x_axis_value_size'])
            ),
            yaxis=dict(
                tickfont=dict(size=settings['y_axis_value_size'])
            )
        )
        return fig, settings['graph_title']
    
    elif chart_type == 'ヒートマップ':
        # FFTヒートマップの作成
        heatmap = go.Heatmap(z=df.values, 
                            x=df.columns, 
                            y=df.index, 
                            colorscale='Viridis')

        # グラフレイアウトの作成
        layout = go.Layout(
            title={'text': settings['graph_title'], 'x': 0.5, 'xanchor': 'center', 'font': {'size': settings['title_font_size']}},
            xaxis_title={'text': settings['x_axis_title'], 'font': {'size': settings['x_axis_title_font_size']}},
            yaxis_title={'text': settings['y_axis_title'], 'font': {'size': settings['y_axis_title_font_size']}},
            xaxis=dict(
                tickfont=dict(size=settings['x_axis_value_size'])
            ),
            yaxis=dict(
                tickfont=dict(size=settings['y_axis_value_size'])
            )
        )
        # 図の作成
        fig = go.Figure(data=[heatmap], layout=layout)
        return fig, settings['graph_title']

    return None, None


def create_fft_plot(freqs, amp_df):
    """Create a line plot of FFT results."""
    colors = px.colors.qualitative.Light24
    fig = go.Figure()
    for i, col in enumerate(amp_df.columns):
        fig.add_trace(
            go.Scatter(x=freqs, y=amp_df[col], mode="lines", name=col, marker=dict(color=colors[i]))
        )
    fig.update_layout(
        title={"text": "FFT結果", "x": 0.5, "xanchor": "center"},
        xaxis_title="周波数(Hz)",
        yaxis_title="加速度",
        xaxis=dict(tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12)),
    )
    return fig
