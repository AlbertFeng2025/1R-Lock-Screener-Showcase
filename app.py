import streamlit as st

# ====================== PAGE CONFIG + DARK THEME ======================
st.set_page_config(
    page_title="The Pattern Trader - Login",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme + brand colors
st.markdown("""
    <style>
    .stApp { background-color: #1C2B3A; color: #FFFFFF; }
    .stHeader, .stToolbar { background-color: #1C2B3A; }
    h1, h2, h3 { color: #3DD68C !important; }
    .stButton>button { background-color: #3DD68C; color: #1C2B3A; font-weight: bold; }
    .stButton>button:hover { background-color: #38D2DC; color: #1C2B3A; }
    </style>
""", unsafe_allow_html=True)

# ====================== SESSION STATE INITIALIZATION ======================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("🌟 The Pattern Trader LLC")
st.markdown("<h2 style='color:#3DD68C; text-align:center;'>1R Lock™ Stock Screener Suite — Showcase</h2>", unsafe_allow_html=True)

# ====================== LOGIN LOGIC ======================
if not st.session_state.logged_in:
    st.subheader("🔑 Member Login (Demo)")
    col1, col2 = st.columns([1, 2])
    with col1:
        username = st.text_input("Username", value="demo")
        password = st.text_input("Password", value="", type="password")
        
        if st.button("Login", type="primary"):
            if username == "demo" and password == "pattern123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Wrong credentials")
    st.caption("Demo → Username: **demo** | Password: **pattern123**")

else:
    # What they see after logging in on the main page
    st.success("✅ Logged in as Demo Member")
    st.info("👈 Please select a screener from the sidebar menu to the left to begin.")
    
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()