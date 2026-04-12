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
    # Tabs for selecting sheet
    tab1, tab2 = st.tabs(["Portfolio Overview", "Dictionary"])

    with tab1:
        df = fetch_sheet_data(SCRIPT_URL, SHEET_NAME)
        if df is not None:
            st.dataframe(df, use_container_width=True)

    with tab2:
        d_df = fetch_sheet_data(SCRIPT_URL, DICT_SHEET_NAME)
        if d_df is not None:
            st.dataframe(d_df, use_container_width=True)

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.login_error = ""
    try:
        st.experimental_rerun()
    except AttributeError:
        st.rerun()


if __name__ == "__main__":
    import login
    login.main()