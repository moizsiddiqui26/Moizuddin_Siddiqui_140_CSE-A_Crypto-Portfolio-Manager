import streamlit as st
from services.crypto_api import get_historical_data

# FIX: Use relative imports to avoid the ImportError
from .pages.dashboard_page import render_dashboard
from .pages.portfolio_page import render_portfolio
from .pages.forecast_page import render_forecast
from .pages.risk_page import render_risk
from .pages.signals_page import render_signals
from .pages.charts_page import render_advanced_charts
from .pages.chatbot_page import render_chatbot_page
from ui.pages.charts_page import render_advanced_charts
@st.cache_data(ttl=300)
def load_data():
    return get_historical_data()

def main():
    page = st.session_state.get("page", "📊 Dashboard")
    df = load_data()

    if df is None or df.empty:
        st.error("Failed to load data")
        return

    if page == "📊 Dashboard":
        render_dashboard(df)
    elif page == "🕯 Advance Chart":
        # This calls the file you uploaded!
        render_advanced_charts(df)
    elif page == "👤 Portfolio":
        render_portfolio(df)
    elif page == "🔮 Forecast":
        render_forecast(df)
    elif page == "⚠ Risk":
        render_risk(df)
    elif page == "📈 Trading Signals":
        render_signals(df)
    elif page == "📉 Advanced Charts":
        render_advanced_charts(df)    
    elif page == "🤖 AI Assistant":
        render_chatbot_page(df)
