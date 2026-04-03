import streamlit as st
import pandas as pd
from finvizfinance.screener.overview import Overview
from datetime import datetime

# ====================== PAGE CONFIG ======================
st.set_page_config(page_title="01 Best Winners", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1C2B3A; color: #FFFFFF; }
    .stHeader, .stToolbar { background-color: #1C2B3A; }
    h1, h2, h3 { color: #3DD68C !important; }
    .stButton>button { background-color: #3DD68C; color: #1C2B3A; font-weight: bold; }
    .stButton>button:hover { background-color: #38D2DC; color: #1C2B3A; }
    .stDataFrame { background-color: #16212E; }
    .stSuccess { color: #3DD68C; }
    </style>
""", unsafe_allow_html=True)

# ====================== SECURITY GATE ======================
# If they are not logged in, stop the script and tell them to go back
if not st.session_state.get("logged_in"):
    st.warning("🔒 Please log in from the main page first.")
    st.stop()

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("### Navigation")
    if st.button("🚪 Logout", key="logout_btn_01"):
        st.session_state.logged_in = False
        st.switch_page("app.py") # Sends them back to the main login screen

# ====================== SCREENER LOGIC ======================
st.header("01 Best Winners")
st.markdown("**Multi-timeframe momentum leaders — highest-conviction long setups**")
st.caption("End-of-Day Scan • Showcase Version")

with st.spinner("Fetching latest stocks from Finviz..."):
    try:
        foverview = Overview()
        filters_dict = {
            'Price': 'Over $5',
            'Average Volume': 'Over 100K',
        }
        foverview.set_filter(filters_dict=filters_dict)
        
        df = foverview.screener_view(limit=100, sleep_sec=0.5)

        if df.empty:
            st.warning("No stocks returned right now.")
            st.stop()

        if 'Average Volume' in df.columns:
            avg_vol_col = 'Average Volume'
        elif 'Avg Volume' in df.columns:
            avg_vol_col = 'Avg Volume'
        else:
            avg_vol_col = None

        df['Dollar Volume (today)'] = df['Price'] * df['Volume']
        if avg_vol_col:
            df['Dollar Volume (30D avg)'] = df['Price'] * df[avg_vol_col]
        else:
            df['Dollar Volume (30D avg)'] = 0

        if 'Performance' in df.columns:
            df = df.sort_values('Performance', ascending=False)
        else:
            df = df.sort_values('Price', ascending=False)

        display_cols = [
            'Ticker', 'Company', 'Sector', 'Price', 'Change', 
            'Volume', 'Rel Volume', 'Performance', 'Average True Range'
        ]
        
        available_cols = [col for col in display_cols if col in df.columns]
        df_display = df[available_cols].copy()

        st.success(f"✅ Found {len(df_display)} stocks")

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Change": st.column_config.NumberColumn("Change %", format="%.2f%%"),
                "Rel Volume": st.column_config.NumberColumn(format="%.2f×"),
                "Performance": st.column_config.NumberColumn(format="%.2f%%"),
                "Average True Range": st.column_config.NumberColumn("ATR", format="%.2f"),
            }
        )

        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export to CSV",
            data=csv,
            file_name="01_Best_Winners.csv",
            mime="text/csv",
        )

        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ET")

    except Exception as e:
        st.error(f"Error: {str(e)}")