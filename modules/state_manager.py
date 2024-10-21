# modules/state_manager.py
import streamlit as st

def initialize_session_state(keys_defaults):
    for key, default_value in keys_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
