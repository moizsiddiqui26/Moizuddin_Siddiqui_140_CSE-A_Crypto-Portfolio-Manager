import streamlit as st
import time

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="CryptoPort AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- NEW: HIDE STREAMLIT HEADER & FOOTER ---
# This removes the top bar and "Deploy" button for a professional look
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stAppDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# ============================================================
# IMPORTS
# ============================================================
from auth.auth_service import login_user, register_user
from ui.components import render_header, render_ticker
from ui import dashboard
from services.live_prices import get_live_prices
from services.alert_engine import check_alerts
from services.email_service import send_welcome_email
from db.database import init_db

# ============================================================
# INITIALIZE DATABASE
# ============================================================
init_db()

# ============================================================
# SESSION STATE
# ============================================================
if "auth" not in st.session_state:
    st.session_state.auth = False

if "mode" not in st.session_state:
    st.session_state.mode = "login"

if "prices" not in st.session_state:
    st.session_state.prices = {}

if "last_update" not in st.session_state:
    st.session_state.last_update = 0

if "page" not in st.session_state:
    st.session_state.page = "📊 Dashboard"

if "email" not in st.session_state:
    st.session_state.email = ""

if "name" not in st.session_state:
    st.session_state.name = ""

# ============================================================
# LOGIN / REGISTER UI
# ============================================================
def login_ui():
    # FIXED: Cleaned up HTML string to prevent raw code rendering
    st.markdown("""
        <div style="text-align:center; padding-top:40px; padding-bottom:20px;">
            <div style="font-size:52px; font-weight:900; color:white;">
                🚀 CRYPTOPORT
            </div>
            <div style="color:#94A3B8; font-size:16px; margin-top:5px;">
                AI-Powered Crypto Intelligence
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 4, 2])

    with col2:
        # --- LOGIN MODE ---
        if st.session_state.mode == "login":
            st.markdown('<h2 style="text-align:center;">🔐 Login</h2>', unsafe_allow_html=True)

            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("🚀 Login", use_container_width=True):
                if not email or not password:
                    st.warning("Please fill all fields.")
                else:
                    result = login_user(email, password)
                    if result["success"]:
                        st.session_state.auth = True
                        st.session_state.email = email
                        if "user" in result:
                            st.session_state.name = result["user"]["name"]
                        st.success("Login Successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(result["msg"])

            if st.button("📝 Create Account", use_container_width=True):
                st.session_state.mode = "register"
                st.rerun()

        # --- REGISTER MODE ---
        else:
            st.markdown('<h2 style="text-align:center;">📝 Register</h2>', unsafe_allow_html=True)

            new_name = st.text_input("Full Name", key="reg_name")
            new_email = st.text_input("Choose Email", key="reg_email")
            new_password = st.text_input("Choose Password", type="password", key="reg_pass")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_conf")

            if st.button("✅ Create Account", use_container_width=True):
                if not new_name or not new_email or not new_password:
                    st.warning("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match!")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    result = register_user(new_name, new_email, new_password)
                    if result["success"]:
                        st.success("✅ Account created successfully!")
                        # Trigger Welcome Email
                        try:
                            send_welcome_email(new_email)
                        except Exception as e:
                            print(f"Email Error: {e}")
                        
                        time.sleep(1)
                        st.session_state.mode = "login"
                        st.rerun()
                    else:
                        st.error(result["msg"])

            if st.button("⬅ Back to Login", use_container_width=True):
                st.session_state.mode = "login"
                st.rerun()

# ============================================================
# MAIN APP
# ============================================================
def main_app():
    render_header(st.session_state.email)

    current_time = time.time()
    # Auto refresh prices every 5 seconds
    if current_time - st.session_state.last_update > 5:
        try:
            st.session_state.prices = get_live_prices()
            st.session_state.last_update = current_time
        except Exception as e:
            print(f"Price Fetch Error: {e}")

    prices = st.session_state.prices

    # ALERTS + TICKER
    if prices:
        try:
            check_alerts(prices)
        except Exception as e:
            print(f"Alert Error: {e}")
        render_ticker(prices)

    # Route to dashboard logic
    dashboard.main()

# ============================================================
# APP ENTRY
# ============================================================
if not st.session_state.auth:
    login_ui()
else:
    main_app()
