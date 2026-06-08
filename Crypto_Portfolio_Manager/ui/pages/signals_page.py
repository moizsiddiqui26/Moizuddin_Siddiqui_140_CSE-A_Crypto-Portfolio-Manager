import streamlit as st
from services.trading_signals import generate_buy_sell_signals

def render_signals(df):
    st.markdown('<div class="section-title">📈 AI Trading Signals</div>', unsafe_allow_html=True)

    # ==========================================
    # 📘 NEW: USER GUIDE SECTION
    # ==========================================
    with st.expander("📖 How to use these signals?", expanded=False):
        st.markdown("""
        **Welcome to the CryptoPort AI Signal Engine!**
        Our system uses a combination of the **Relative Strength Index (RSI)** and **Moving Average Trends** to provide real-time guidance.
        
        * **BUY**: Indicates the asset is oversold or starting a strong upward momentum.
        * **SELL**: Indicates the asset is overbought or starting a downward trend.
        * **HOLD**: The market is neutral or stable; wait for a clearer trend.
        
        *⚠️ Disclaimer: AI signals are for educational purposes. Always perform your own risk assessment before trading.*
        """)

    # ==========================================
    # 🔍 SELECTION & CALCULATION
    # ==========================================
    coins = sorted(df["Crypto"].unique())
    
    col1, col2 = st.columns([2, 1])
    with col1:
        coin = st.selectbox("Select Asset to Analyze", coins)
    
    coin_df = df[df["Crypto"] == coin]
    result = generate_buy_sell_signals(coin_df)

    # ==========================================
    # 💎 ENHANCED UI DISPLAY
    # ==========================================
    st.markdown("---")
    
    # Dynamic styling for the Signal
    signal_type = result["signal"].upper()
    signal_color = "#00ffcc" if signal_type == "BUY" else "#ff4b4b" if signal_type == "SELL" else "#94A3B8"
    
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.markdown(f"### Current Signal\n<h1 style='color:{signal_color}; margin-top:0;'>{signal_type}</h1>", unsafe_allow_html=True)
    
    with m_col2:
        # RSI Indicator with a helpful label
        rsi_val = result["rsi"]
        rsi_status = "Oversold" if rsi_val < 30 else "Overbought" if rsi_val > 70 else "Neutral"
        st.metric("RSI (14)", f"{rsi_val:.2f}", help=f"RSI < 30 is Oversold, > 70 is Overbought. Currently {rsi_status}.")
        
    with m_col3:
        st.metric("Market Trend", result["trend"])

    # AI Reason Breakdown
    st.info(f"**AI Analysis:** {result['reason']}")

    # ==========================================
    # 📘 RSI KNOWLEDGE CENTER (Bottom Section)
    # ==========================================
    st.markdown("---")
    st.markdown("### 🎓 Understanding RSI (Relative Strength Index)")
    
    # Using columns to create a clean "Cheat Sheet"
    guide_col1, guide_col2 = st.columns(2)

    with guide_col1:
        st.write("**What is RSI?**")
        st.caption("""
        The RSI is a momentum oscillator that measures the speed and change of price movements. 
        It ranges from **0 to 100**. It is primarily used to identify 'Overbought' or 'Oversold' 
        conditions in an asset.
        """)
        
    with guide_col2:
        st.write("**The Range Guide**")
        st.markdown("""
        - 🟢 **Below 30 (Oversold):** The asset may be undervalued. Potential Buying opportunity.
        - ⚪ **40 to 60 (Neutral):** Consolidation zone. No clear trend.
        - 🔴 **Above 70 (Overbought):** The asset may be overvalued. Potential Selling opportunity.
        """)

