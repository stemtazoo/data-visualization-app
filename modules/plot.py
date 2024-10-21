import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# colors = [
#     "#0068c9", "#83c9ff", "#ff2b2b", "#ffabab",
#     "#29b09d", "#7defa1", "#ff8700", "#ffd16a",
#     "#6d3fc0", "#d5dae5"
# ]

# def create_plot(chart_type, df, settings):
#     if chart_type in ["折れ線グラフ", "棒グラフ", "散布図", "ヒートマップ"]:
#         add_color = st.checkbox("凡例を追加する（color）", value=False)
#         color = st.selectbox("凡例の列を選択", [None] + df.columns.tolist(), key="color_selectbox") if add_color else None

#         if chart_type == "折れ線グラフ":
#             fig = px.line(df, x=settings['x_axis'], y=settings['y_axis'], color=color, title=settings['graph_title'], color_discrete_sequence=colors)
#         elif chart_type == "棒グラフ":
#             fig = px.bar(df, x=settings['x_axis'], y=settings['y_axis'], color=color, title=settings['graph_title'], color_discrete_sequence=colors)
#         elif chart_type == "散布図":
#             fig = px.scatter(df, x=settings['x_axis'], y=settings['y_axis'], color=color, title=settings['graph_title'], color_discrete_sequence=colors)
#         elif chart_type == "ヒートマップ":
#             z_axis = st.selectbox("Z軸を選択", df.columns, key="z_axis_selectbox")
#             fig = px.density_heatmap(df, x=settings['x_axis'], y=settings['y_axis'], z=z_axis, title=settings['graph_title'], color_continuous_scale=colors)

#         fig.update_layout(
#             title={'text': settings['graph_title'], 'x':0.5, 'xanchor': 'center', 'font': {'size': settings['title_font_size']}},
#             xaxis_title={'text': settings['x_axis_title'], 'font': {'size': settings['x_axis_title_font_size']}},
#             yaxis_title={'text': settings['y_axis_title'], 'font': {'size': settings['y_axis_title_font_size']}},
#             xaxis=dict(
#                 tickfont=dict(size=settings['x_axis_value_size'])
#             ),
#             yaxis=dict(
#                 tickfont=dict(size=settings['y_axis_value_size'])
#             )
#         )
#         return fig, settings['graph_title']

#     elif chart_type == "ヒストグラム":
#         numeric_columns = df.select_dtypes(include='number').columns.tolist()
#         if not numeric_columns:
#             st.warning("ヒストグラムを作成するには、数値列が必要です。")
#             return None, None

#         column = st.selectbox("列を選択", numeric_columns, key="histogram_column_selectbox")
#         add_color = st.checkbox("凡例を追加する（color）", key="histogram_add_color_checkbox")
#         color = st.selectbox("凡例の列を選択", [None] + df.columns.tolist(), key="histogram_color_selectbox") if add_color else None

#         fig = px.histogram(df, x=column, color=color, title=settings['graph_title'], color_discrete_sequence=colors)
#         fig.update_layout(
#             title={'text': settings['graph_title'], 'x':0.5, 'xanchor': 'center', 'font': {'size': settings['title_font_size']}},
#             xaxis_title={'text': settings['x_axis_title'], 'font': {'size': settings['x_axis_title_font_size']}},
#             yaxis_title={'text': settings['y_axis_title'], 'font': {'size': settings['y_axis_title_font_size']}},
#             xaxis=dict(
#                 tickfont=dict(size=settings['x_axis_value_size'])
#             ),
#             yaxis=dict(
#                 tickfont=dict(size=settings['y_axis_value_size'])
#             )
#         )
#         return fig, settings['graph_title']

#     return None, None

# グラフ生成関数の定義
def create_plot(chart_type, df, settings):
    colors = [
        "#0068c9", "#83c9ff", "#ff2b2b", "#ffabab",
        "#29b09d", "#7defa1", "#ff8700", "#ffd16a",
        "#6d3fc0", "#d5dae5"
    ]

    if chart_type in ["折れ線グラフ", "棒グラフ", "散布図", "ヒートマップ"]:
        add_color = st.checkbox("凡例を追加する（color）", value=False)
        color = st.selectbox("凡例の列を選択", [None] + df.columns.tolist(), key="color_selectbox") if add_color else None

        if chart_type == "折れ線グラフ":
            if settings['use_secondary_y'] and settings['secondary_y_axis']:
                fig = go.Figure()
                for y in settings['y_axis']:
                    fig.add_trace(go.Scatter(x=df[settings['x_axis']], y=df[y], mode='lines', name=y))
                for y in settings['secondary_y_axis']:
                    fig.add_trace(go.Scatter(x=df[settings['x_axis']], y=df[y], mode='lines', name=y, yaxis='y2'))
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
        elif chart_type == "ヒートマップ":
            z_axis = st.selectbox("Z軸を選択", df.columns, key="z_axis_selectbox")
            fig = px.density_heatmap(df, x=settings['x_axis'], y=settings['y_axis'], z=z_axis, title=settings['graph_title'], color_continuous_scale=colors)

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

    return None, None