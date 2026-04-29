import streamlit as st
import pandas as pd
from data_formatter import format_dataframe_for_display, style_dataframe


def display_all_sheets(script_url: str, fetch_sheet_data_func):
    """Dynamically display all available sheets from Google Sheets as tabs."""
    try:
        # Fetch all sheet names
        params = {"action": "sheets"}
        import requests
        response = requests.get(script_url, params=params)
        response.raise_for_status()
        sheet_names = response.json()
        
        if not sheet_names:
            st.info("No sheets found in the Google Sheet.")
            return
        
        # Create tabs dynamically for all sheets
        tabs = st.tabs(sheet_names)
        
        for idx, sheet_name in enumerate(sheet_names):
            with tabs[idx]:
                st.subheader(sheet_name)
                df = fetch_sheet_data_func(script_url, sheet_name)
                if df is not None:
                    df_formatted = format_dataframe_for_display(df, sheet_name)
                    st.dataframe(style_dataframe(df_formatted), use_container_width=True, hide_index=True)
                else:
                    st.warning(f"Could not fetch data from sheet: {sheet_name}")
    
    except Exception as e:
        st.error(f"Error displaying sheets: {e}")
