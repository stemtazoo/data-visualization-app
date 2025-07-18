import base64
import io

import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

# データフレームを表示する。
def show_dataframe(df, title='See data!'):
    with st.expander(title):
        st.dataframe(df)

# Auto Filter Dataframes in streamlit
def filter_dataframe(df: pd.DataFrame, key='origin') -> pd.DataFrame:
    #test
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters", key=key)

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 20:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                if column == '機番':
                    _min = df[column].min().item()
                    _max = df[column].max().item()
                    step = 1
                else:
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

# chartをhtmlファイルでダウンロード
def download_chart_html(fig, title, key='download_chart_html'):
    '''
    download a plotly chart as a htmlfile
    
    Args:
        fig : plotly chart
        title : filename str
    Returns:
         :
     
    '''
    html_buff=io.StringIO()
    fig.write_html(html_buff, include_plotlyjs='cdn')
    html_bytes = html_buff.getvalue().encode()
    st.download_button(
        label = 'Download Chart',
        data = html_bytes,
        file_name = title + '.html',
        mime = 'text/html', 
        key = key
    )

# 日本語を含むCSVファイルのダウンロード
def download_csv_jis(df,title):
    '''
    Download data frames containing Japanese as CSV files.
    
    Args:
        df : pandas dataframe
        title : file name str
    Returns:
         :
     
    '''
    csv = df.to_csv(encoding='utf_8_sig')
    b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download= "{title}.csv">Download Link</a>'
    st.markdown(f"Download data as CSV:  {href}", unsafe_allow_html=True)

# データを更新する。
def update_data():
    if st.button("データ更新"):
        # Clear values from *all* all in-memory and on-disk data caches:
        # i.e. clear values from both square and cube
        st.cache_data.clear()