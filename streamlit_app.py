import streamlit as st
import pandas as pd
import requests

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzf0WEFtEKQo5dTCaTun5efjQtR4sZU95QcaJzjjbNX2-16-TS0BOZbCoBsi5MLX9Iv/exec"
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

def save_sheet_data(script_url: str, sheet_name: str, data: list):
    try:
        payload = {"sheetName": sheet_name, "data": data}
        response = requests.post(script_url, json=payload)
        response.raise_for_status()
        result = response.json()
        if "error" in result:
            st.error(result["error"])
            return False
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def render_data_viewer(username: str):
    # Header with logout button
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title("My Portfolio")
    with col2:
        st.write("")
        st.write(f"**User**: {username}")
    with col3:
        st.write("")
        if st.button("Logout", key="logout_btn"):
            logout()
    
    st.divider()
    
    # Tabs for viewing and adding data
    tab1, tab2, tab3 = st.tabs(["Portfolio Overview", "Dictionary", "Add Data"])

    with tab1:
        df = fetch_sheet_data(SCRIPT_URL, SHEET_NAME)
        if df is not None:
            st.dataframe(df, use_container_width=True)

    with tab2:
        d_df = fetch_sheet_data(SCRIPT_URL, DICT_SHEET_NAME)
        if d_df is not None:
            st.dataframe(d_df, use_container_width=True)

    with tab3:
        st.subheader("Add New Data")
        sheet_names = ["Robinhood", "ZerodhaUMF"]
        sheet_choice = st.selectbox("Select Sheet", sheet_names, key="sheet_choice")
        
        def lookup_fund():
            id_val = st.session_state.get("id_input", "").strip()
            if id_val:
                d_df = fetch_sheet_data(SCRIPT_URL, DICT_SHEET_NAME)
                if d_df is not None:
                    # Assume columns are named "ID" and "FUND NAME"
                    if "ID" in d_df.columns and "FUND NAME" in d_df.columns:
                        row = d_df[d_df["ID"].astype(str) == id_val]
                        if not row.empty:
                            st.session_state.fund_name = str(row["FUND NAME"].values[0])
                        else:
                            st.session_state.fund_name = ""
                    else:
                        st.error("Dictionary sheet must have 'ID' and 'FUND NAME' columns.")
                        st.session_state.fund_name = ""
                else:
                    st.session_state.fund_name = ""
            else:
                st.session_state.fund_name = ""
        
        id_input = st.text_input("ID", key="id_input", on_change=lookup_fund)
        fund_name = st.text_input("Fund Name", value=st.session_state.get('fund_name', ''), key="fund_name_input")
        trade_date = st.date_input("Trade Date")
        quantity = st.number_input("Quantity", step=1)
        price = st.number_input("Price", step=0.01)
        amount = st.number_input("Amount", step=0.01)
        
        if st.button("Add Data"):
            data_list = [[id_input, fund_name, str(trade_date), quantity, price, amount]]
            if save_sheet_data(SCRIPT_URL, sheet_choice, data_list):
                st.success("Data added successfully!")
                try:
                    st.experimental_rerun()
                except AttributeError:
                    st.rerun()
            else:
                st.error("Failed to add data.")

def get_sheet_names(script_url: str):
    try:
        params = {"action": "sheets"}
        response = requests.get(script_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        st.error(f"Error fetching sheet names: {e}")
        return [SHEET_NAME, DICT_SHEET_NAME]  # fallback


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