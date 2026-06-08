import streamlit as st

# ======================================================
# HEADER COMPONENT
# ======================================================
def render_header(user_email):

    # Default page
    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    # ==================================================
    # FULL-WIDTH CSS RESET & CUSTOM STYLES
    # ==================================================
    st.markdown("""
    <style>
    /* 1. FORCE REMOVE ALL STREAMLIT PADDING AND MARGINS */
    [data-testid="stAppViewContainer"] > section:nth-child(2) > div:nth-child(1) {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }

    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }

    /* Hide Streamlit Sidebar and Top Header */
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    header {
        visibility: hidden;
    }

    /* 2. Main Header: Zero Gap Styling */
    .custom-header {
        background: linear-gradient(90deg, #0f0c29, #302b63, #24243e);
        padding: 25px 40px;
        /* Remove radius for flush look against screen edges */
        border-radius: 0px; 
        border-bottom: 2px solid #00ffcc;
        margin-top: 0px !important;
        margin-left: 0px !important;
        margin-right: 0px !important;
        width: 100%;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.45);
    }

    /* Top Row Layout */
    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }

    /* Logo Styling */
    .header-title {
        color: white;
        font-size: 34px;
        font-weight: 800;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Inter', sans-serif;
    }

    .elite-tag {
        color: #94A3B8;
        font-size: 11px;
        letter-spacing: 2px;
        font-weight: 500;
        margin-left: 5px;
    }

    /* User Badge */
    .user-badge {
        background: rgba(255, 255, 255, 0.08);
        padding: 10px 18px;
        border-radius: 25px;
        color: #00ffcc;
        font-size: 14px;
        font-weight: 600;
        border: 1px solid rgba(0, 255, 204, 0.35);
        display: flex;
        align-items: center;
        gap: 10px;
        backdrop-filter: blur(8px);
    }

    /* Status Pulse */
    .status-dot {
        width: 10px;
        height: 10px;
        background: #00ffcc;
        border-radius: 50%;
        box-shadow: 0 0 10px #00ffcc;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 12px rgba(0, 255, 204, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); }
    }

    /* Navigation Bar Spacing (Slight padding so buttons aren't flush) */
    .nav-wrapper {
        padding: 15px 20px;
    }

    /* Navigation Buttons */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.03);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 10px;
        font-weight: 500;
        transition: 0.3s ease;
    }

    div.stButton > button:hover {
        border: 1px solid #00ffcc;
        color: #00ffcc;
        transform: translateY(-2px);
        box-shadow: 0 0 12px rgba(0, 255, 204, 0.25);
    }
    </style>
    """, unsafe_allow_html=True)

    # ==================================================
    # HEADER HTML
    # ==================================================
    header_html = f"""
    <div class="custom-header">
        <div class="header-top">
            <div class="header-title">
                🚀 CRYPTOPORT
                <span class="elite-tag"></span>
            </div>
            <div class="user-badge">
                <span class="status-dot"></span>
                <span>LIVE</span>
                <span>|</span>
                <span>👤 {user_email}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # ==================================================
    # NAVIGATION MENU
    # ==================================================
    # Use a container div for the buttons to add horizontal padding
    st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6, col7,col8 = st.columns(8)

    with col1:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.page = "📊 Dashboard"
            st.rerun()
    with col2:
        if st.button("🕯 Advance Chart", use_container_width=True):
            st.session_state.page = "🕯 Advance Chart"
            st.rerun()    
    with col3:
        if st.button("📈 Signals", use_container_width=True):
            st.session_state.page = "📈 Trading Signals"
            st.rerun()
    with col4:
        if st.button("🔮 Forecast", use_container_width=True):
            st.session_state.page = "🔮 Forecast"
            st.rerun()
    with col5:
        if st.button("⚠ Risk", use_container_width=True):
            st.session_state.page = "⚠ Risk"
            st.rerun()
    with col6:
        if st.button("👤 Portfolio", use_container_width=True):
            st.session_state.page = "👤 Portfolio"
            st.rerun()
    with col7:
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.session_state.page = "🤖 AI Assistant"
            st.rerun()
    with col8:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ======================================================
# TICKER COMPONENT
# ======================================================
def render_ticker(prices):
    if not prices:
        return

    ticker_items = ""
    for coin, details in prices.items():
        price = details["price"]
        change = details["change_24h"]
        color = "#00ffcc" if change >= 0 else "#ff4b4b"
        symbol = "▲" if change >= 0 else "▼"

        ticker_items += f"""
        <span style="margin-right:40px;font-weight:bold;">
            {coin.upper()}:
            <span style="color:white;">${price:,.2f}</span>
            <span style="color:{color};">{symbol} {abs(change):.2f}%</span>
        </span>
        """

    st.markdown(f"""
    <div style="
        background:rgba(255,255,255,0.04);
        padding:10px 20px;
        border-radius:0px;
        overflow:hidden;
        margin-bottom:20px;
        border-top:1px solid rgba(255,255,255,0.06);
        border-bottom:1px solid rgba(255,255,255,0.06);
    ">
        <marquee scrollamount="5" style="color:white; font-family:monospace; font-size:14px;">
            {ticker_items}
        </marquee>
    </div>
    """, unsafe_allow_html=True)
