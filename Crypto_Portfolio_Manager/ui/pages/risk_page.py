import streamlit as st
from services.risk_engine import (
    run_risk_analysis,
    calculate_portfolio_risk
)

def render_risk(df):
    st.markdown("# ⚠ Portfolio Risk Analysis")

    # --- BEGINNER'S WELCOME GUIDE ---
    st.markdown("""
        <div style="background-color: #1a1c23; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B; margin-bottom: 25px;">
            <h4 style="margin-top:0;">🛡️ New to Risk Management?</h4>
            <p style="color: #A1A7BB; font-size: 14px;">
                In crypto, "Risk" isn't just about losing money—it's about how much a coin's price "bounces" (Volatility). 
                A <b>High Risk</b> coin might make you a lot of money fast, but it can also drop just as quickly.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Risk Analysis Logic
    risk_df = run_risk_analysis(df)
    
    st.subheader("📊 Individual Asset Risk")
    st.dataframe(
        risk_df, 
        column_config={
            "Volatility": st.column_config.NumberColumn(format="%.2f%%"),
            "Risk Score": st.column_config.ProgressColumn(min_value=0, max_value=100)
        },
        use_container_width=True,
        hide_index=True
    )

    # Portfolio Summary
    st.markdown("---")
    st.subheader("💼 Your Overall Portfolio Health")
    portfolio = calculate_portfolio_risk(df)

    col1, col2 = st.columns(2)
    
    # Use color-coded metrics for clarity
    risk_level = portfolio["level"]
    color = "inverse" if risk_level == "High" else "normal"
    
    col1.metric("Risk Level", risk_level, delta=risk_level, delta_color=color)
    col2.metric("Risk Score", f"{portfolio['score']}/100")

    # --- NEW USER EDUCATION SECTION ---
    st.markdown("---")
    st.subheader("📚 How to read these results")
    
    with st.expander("🔍 What does 'Volatility' mean?"):
        st.write("""
        Imagine a car's speed. 
        - **Low Volatility:** A steady car driving at 60mph. You know where you'll be in an hour.
        - **High Volatility:** A roller coaster. One second you're at the top, the next you're dropping at 100mph. 
        Most cryptocurrencies have **High Volatility** compared to traditional stocks.
        """)
        

    with st.expander("📉 What is a 'Risk Score'?"):
        st.write("""
        We calculate this score (0-100) based on how often a coin's price crashes versus how much it grows.
        - **0-30 (Low):** Generally safer, "Blue Chip" coins like Bitcoin.
        - **31-70 (Medium):** Established coins with more room for movement.
        - **71-100 (High):** Very "bouncy" coins. Great for quick gains, but very dangerous for long-term savings.
        """)

    st.success("💡 **Pro Tip:** If your Risk Level is 'High', consider adding some 'Stablecoins' (coins pegged to the US Dollar) to balance your portfolio.")
