# modules/state_manager.py
import json
import os
import importlib.resources as pkg_resources

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

# 設定ファイルの読み込み
def load_config():
    with pkg_resources.open_text('config', 'config.json') as f:
        return json.load(f)
    
def get_user_settings_path():
    # Windows の場合、ユーザーのドキュメントフォルダに保存する
    if os.name == 'nt':
        user_documents = os.path.join(os.path.expanduser('~'), 'Documents')
    else:
        # 他のシステム (Linux, macOS) の場合はホームディレクトリに保存する
        user_documents = os.path.expanduser('~')
        
    # ユーザー設定ファイルの完全なパスを指定
    user_settings_path = os.path.join(user_documents, 'user_settings.json')
    
    return user_settings_path

def save_user_settings(settings):
    user_settings_path = get_user_settings_path()
    
    try:
        with open(user_settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
            st.success("設定が保存されました！")
    except Exception as e:
        st.error(f"設定の保存に失敗しました: {e}")

def load_user_settings():
    user_settings_path = get_user_settings_path()

    if os.path.exists(user_settings_path):
        try:
            with open(user_settings_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"設定の読み込みに失敗しました: {e}")
            return {}
    else:
        return {}

def merge_settings(default_settings, user_settings):
    # default_settingsの各キーに対して、user_settingsの値が存在する場合はそれを上書き
    if len(user_settings) > 0:
        for key, value in user_settings.items():
            if key in default_settings and isinstance(value, type(default_settings[key])):
                default_settings[key] = value
    return default_settings