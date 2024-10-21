import io
import streamlit as st

def download_chart_html(fig, title):
    html_buff = io.StringIO()
    fig.write_html(html_buff, include_plotlyjs='cdn')
    html_bytes = html_buff.getvalue().encode()
    st.download_button(
        label='Download Chart',
        data=html_bytes,
        file_name=title + '.html',
        mime='text/html'
    )
