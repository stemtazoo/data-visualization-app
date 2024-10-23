# modules/state_manager.py
import streamlit as st

def initialize_session_state(keys_defaults):
    for key, default_value in keys_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
        
def reset_session_state_to_default(config):
    """
    Reset st.session_state values to the default settings provided in the config.

    Args:
    config (dict): The configuration dictionary containing default settings.
    """
    default_settings = config.get('default_settings', {})
    
    # Iterate over the default settings and set them in st.session_state
    for key, value in default_settings.items():
        st.session_state[key] = value

def apply_user_settings(user_settings):
    """
    Update st.session_state values with user_settings values.

    Args:
    user_settings (dict): The dictionary containing user settings.
    """
    # Iterate over the user settings and set them in st.session_state
    for key, value in user_settings.items():
        st.session_state[key] = value