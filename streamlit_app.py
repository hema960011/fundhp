import streamlit as st
import pandas as pd
import requests

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyMWXdHXnLfM0ijwaUAFgxBZgHdXoXFSa6BDaBQlT4VfC9E_PzWVsf0Znguj72rombh/exec"
SHEET_NAME = "Portfolio Overview"
DICT_SHEET_NAME = "Dictionary"

def fetch_sheet_data(script_url: str, sheet_name: str):
    try:
        params = {"sheetName": sheet_name}
        response = requests.get(script_url, params=params)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and data.get("error"):
            st.error(data["error"])
            return None
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def render_data_viewer(username: str):
    # Initialize session state for selected sheet
    if "selected_sheet" not in st.session_state:
        st.session_state.selected_sheet = "Portfolio Overview"

    # Buttons to select sheet
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Portfolio Overview", key="portfolio_btn"):
            st.session_state.selected_sheet = "Portfolio Overview"
    with col2:
        if st.button("Dictionary", key="dictionary_btn"):
            st.session_state.selected_sheet = "Dictionary"

    # Display selected sheet data
    if st.session_state.selected_sheet == "Portfolio Overview":
        df = fetch_sheet_data(SCRIPT_URL, SHEET_NAME)
        if df is not None:
            st.subheader(SHEET_NAME)
            st.dataframe(df, use_container_width=True)
    elif st.session_state.selected_sheet == "Dictionary":
        d_df = fetch_sheet_data(SCRIPT_URL, DICT_SHEET_NAME)
        if d_df is not None:
            st.subheader(DICT_SHEET_NAME)
            st.dataframe(d_df, use_container_width=True)

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.login_error = ""
    try:
        st.experimental_rerun()
    except AttributeError:
        st.rerun()