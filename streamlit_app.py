import streamlit as st
import pandas as pd
import requests
import json

# Function to fetch data from Google Apps Script web app
def fetch_sheet_data(script_url, sheet_name):
    try:
        params = {"sheetName": sheet_name}
        response = requests.get(script_url, params=params)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and data.get("error"):
            st.error(data["error"])
            return None
        df = pd.DataFrame(data[1:], columns=data[0])  # First row as headers
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Streamlit app
st.title("Google Sheets Data Viewer (via Apps Script)")

# Input for Apps Script URL and sheet name
script_url = "https://script.google.com/macros/s/AKfycbyMWXdHXnLfM0ijwaUAFgxBZgHdXoXFSa6BDaBQlT4VfC9E_PzWVsf0Znguj72rombh/exec"
sheet_name = "Portfolio Overview"
dict_sheet_name = "Dictionary"

if script_url and sheet_name:
    df = fetch_sheet_data(script_url, sheet_name)
    d_df = fetch_sheet_data(script_url, dict_sheet_name)
    if df is not None:
        st.subheader(f"{sheet_name}")
        st.dataframe(df)

        st.subheader(f"{dict_sheet_name}")
        st.dataframe(d_df)

        # Optional: Show some stats
        #st.subheader("Data Summary")
        #st.write(f"Number of rows: {len(df)}")
        #st.write(f"Number of columns: {len(df.columns)}")
        #st.write("Column names:", list(df.columns))
else:
    st.info("Please enter the Apps Script Web App URL and sheet name to load data.")