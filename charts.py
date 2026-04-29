import streamlit as st
import pandas as pd
from data_formatter import format_dataframe_for_display


def display_portfolio_charts(df):
    """Display charts for portfolio analysis."""
    st.subheader("Portfolio Analysis")
    
    # Convert numeric columns for charting
    try:
        df_chart = df.copy()
        
        # Convert numeric columns
        numeric_cols = ["total invested", "current price", "p/l", "total quantity"]
        for col in df_chart.columns:
            if col.lower().strip() in numeric_cols or col.lower().replace(" ", "") in numeric_cols:
                df_chart[col] = pd.to_numeric(df_chart[col], errors='coerce')
        
        # Set account as index
        account_col = None
        for col in df_chart.columns:
            if col.lower().strip() == "account":
                account_col = col
                break
        
        if account_col:
            df_chart = df_chart.set_index(account_col)
        
        # Find column names dynamically
        total_invested_col = None
        current_price_col = None
        pl_col = None
        total_quantity_col = None
        
        for col in df_chart.columns:
            col_lower = col.lower().strip()
            if "total" in col_lower and "invested" in col_lower:
                total_invested_col = col
            elif "current" in col_lower and "price" in col_lower:
                current_price_col = col
            elif "p/l" in col_lower or col_lower == "pl":
                pl_col = col
            elif "total" in col_lower and "quantity" in col_lower:
                total_quantity_col = col
        
        # Display Total Quantity with precision 2
        if total_quantity_col:
            st.subheader("Total Quantity")
            quantity_data = df_chart[[total_quantity_col]].dropna()
            if not quantity_data.empty:
                quantity_display = quantity_data.copy()
                quantity_display[total_quantity_col] = quantity_display[total_quantity_col].apply(lambda x: f"{x:.2f}")
                st.dataframe(quantity_display, use_container_width=True)
        
        # Display bar charts
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Total Invested vs Current Price")
            if total_invested_col and current_price_col:
                chart_cols = [col for col in [total_invested_col, current_price_col] if col in df_chart.columns]
                if len(chart_cols) == 2:
                    chart_data = df_chart[chart_cols].dropna()
                    if not chart_data.empty:
                        # Ensure all values are numeric
                        chart_data = chart_data.astype(float)
                        st.bar_chart(chart_data)
            else:
                st.info(f"Columns for 'Total Invested' or 'Current Price' not found.")
        
        # Display P/L chart
        with col2:
            st.subheader("Profit/Loss by Account")
            if pl_col:
                pl_data = df_chart[[pl_col]].dropna()
                if not pl_data.empty:
                    pl_data = pl_data.astype(float)
                    st.bar_chart(pl_data)
            else:
                st.info("Column for 'P/L' not found.")
    except Exception as e:
        st.warning(f"Could not generate charts: {e}")



