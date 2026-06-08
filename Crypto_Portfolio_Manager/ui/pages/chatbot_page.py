import streamlit as st
import pandas as pd
import os
import sys

# --- PATH FIX FOR ROBUST IMPORTS ---
dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(dir_path, "../../.."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

try:
    from services.ai_assistant import ask_ai
    from db.models import get_holdings
except ImportError:
    st.error("Error loading backend services.")

def render_chatbot_page(df):
    # Professional Header
    st.markdown('<div class="section-title">🤖 AI Investment Copilot</div>', unsafe_allow_html=True)

    # ============================================================
    # 📘 USER GUIDE
    # ============================================================
    with st.expander("📖 New User Guide: How to use this AI"):
        st.markdown("""
        ### Welcome to your AI Copilot! 
        Think of this AI as your **financial mentor**. It has access to your portfolio and live market trends.
        
        **Things you can ask:**
        - **"Explain Bitcoin like I'm 5"** — Great for understanding the basics.
        - **"Is it a good time to buy Ethereum?"** — AI analyzes the current charts for you.
        - **"How can I lower my portfolio risk?"** — AI suggests safer moves based on your data.
        """)
        st.info("💡 **Pro Tip:** Be specific. Instead of asking 'Is BTC good?', try 'Is BTC a good long-term hold given its current volatility?'")

    st.markdown("---")

    # ============================================================
    # 💬 CHAT INTERFACE (Full Width)
    # ============================================================
    
    # Background Portfolio Sync (Silent)
    email = st.session_state.get("email")
    holdings = get_holdings(email)
    portfolio_summary = "User has no active holdings."
    if holdings:
        pf = pd.DataFrame(holdings, columns=["Crypto", "Amount", "Date"])
        portfolio_summary = pf.to_string()

    # Chat container for scrollable area
    chat_container = st.container(height=500, border=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            ("assistant", "Hello! I'm your AI Crypto Advisor. I've synced with your portfolio and market data. What's on your mind?")
        ]

    # Display history
    with chat_container:
        for role, msg in st.session_state.chat_history:
            with st.chat_message(role):
                st.markdown(msg)

    # Chat Input
    user_input = st.chat_input("Ask your AI crypto advisor...")

    if user_input:
        # Add user message to history
        st.session_state.chat_history.append(("user", user_input))
        
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing market data..."):
                # Portfolio summary is passed to the AI silently
                response = ask_ai(user_input, portfolio_summary)
                st.markdown(response)
                st.session_state.chat_history.append(("assistant", response))
        
        st.rerun()

