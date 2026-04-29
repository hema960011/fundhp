import pandas as pd
import streamlit as st


def format_dataframe_for_display(df, sheet_name=""):
    """
    Format dataframe for display:
    1. Remove unnamed index column and reset index
    2. Remove specific columns from certain sheets
    3. Format numeric columns to 2 decimals (except ID and Quantity)
    4. Format quantity columns to 4 decimals
    5. Format date columns to YYYY-MM-DD
    6. Apply conditional formatting for negative values
    """
    df_display = df.copy()
    
    # Reset index and remove index column
    if df_display.index.name or not all(isinstance(x, int) for x in df_display.index):
        df_display = df_display.reset_index(drop=True)
    
    # Remove unnamed columns
    unnamed_cols = [col for col in df_display.columns if 'Unnamed' in str(col) or str(col).strip() == '']
    df_display = df_display.drop(columns=unnamed_cols, errors='ignore')
    
    # Remove specific columns from certain sheets
    sheets_to_clean = ["Robinhood", "ZerodhaUMF", "ZerodhaHMF"]
    if sheet_name in sheets_to_clean:
        cols_to_remove = [col for col in df_display.columns if "price as of trade" in col.lower()]
        df_display = df_display.drop(columns=cols_to_remove, errors='ignore')
    
    # Convert columns
    for col in df_display.columns:
        col_lower = col.lower().strip()
        
        # Format quantity columns to 4 decimals
        if 'quantity' in col_lower:
            try:
                numeric_series = pd.to_numeric(df_display[col], errors='coerce')
                df_display[col] = numeric_series.apply(lambda x: f"{x:.4f}" if pd.notna(x) else x)
            except:
                pass
            continue
        
        # Skip ID column for decimal formatting
        if 'id' in col_lower:
            continue
        
        # Try to convert to numeric and format to 2 decimals
        if col_lower not in ['id', 'quantity', 'account', 'fund name', 'fund_name']:
            try:
                numeric_series = pd.to_numeric(df_display[col], errors='coerce')
                # Check if most values are numeric
                non_null_count = numeric_series.notna().sum()
                if non_null_count > len(numeric_series) * 0.5:  # At least 50% numeric
                    df_display[col] = numeric_series.apply(lambda x: f"{x:.2f}" if pd.notna(x) else x)
            except:
                pass
        
        # Format date columns
        if 'date' in col_lower or 'trade date' in col_lower:
            try:
                date_series = pd.to_datetime(df_display[col], errors='coerce')
                df_display[col] = date_series.dt.strftime('%Y-%m-%d')
            except:
                pass
    
    return df_display


def highlight_negatives(val):
    """Highlight negative numbers in red."""
    try:
        float_val = float(str(val).replace(',', ''))
        if float_val < 0:
            return 'color: red; font-weight: bold'
    except (ValueError, TypeError):
        pass
    return ''


def style_dataframe(df):
    """Apply styling to dataframe for display."""
    # Apply negative value highlighting
    styled = df.style.map(highlight_negatives)
    return styled
