import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from db.models import add_holding, get_holdings, sell_holding

def render_portfolio(df):
    st.markdown('<div class="section-title">👤 Professional Portfolio Manager</div>', unsafe_allow_html=True)

    email = st.session_state.get("email")
    if not email:
        st.warning("Please log in to view your portfolio.")
        return

    # ==========================================
    # 📊 1. ANALYTICS & TABLE (TOP SECTION)
    # ==========================================
    data = get_holdings(email)

    if not data:
        st.info("No investments yet. Scroll down to add your first transaction!")
    else:
        # Load data from DB
        portfolio_df = pd.DataFrame(data, columns=["Crypto", "Amount", "Date"])
        portfolio_df["Date"] = pd.to_datetime(portfolio_df["Date"])

        # Calculate Current Prices
        latest_prices = df.groupby("Crypto").last().reset_index()[["Crypto", "Close"]]
        latest_prices.rename(columns={"Close": "Current Price"}, inplace=True)
        portfolio_df = portfolio_df.merge(latest_prices, on="Crypto", how="left")

        # Calculate Buy Price based on historical date
        def get_buy_price(row):
            coin_df = df[df["Crypto"] == row["Crypto"]]
            past_data = coin_df[coin_df["Date"] <= row["Date"]]
            return past_data.iloc[-1]["Close"] if not past_data.empty else np.nan

        portfolio_df["Buy Price"] = portfolio_df.apply(get_buy_price, axis=1)

        # Financial Calculations
        portfolio_df["Quantity"] = portfolio_df["Amount"] / portfolio_df["Buy Price"]
        portfolio_df["Current Value"] = portfolio_df["Quantity"] * portfolio_df["Current Price"]
        portfolio_df["Profit ($)"] = portfolio_df["Current Value"] - portfolio_df["Amount"]

        # --- EXECUTIVE SUMMARY ---
        total_invested = portfolio_df["Amount"].sum()
        total_value = portfolio_df["Current Value"].sum()
        total_profit = total_value - total_invested
        profit_pct = (total_profit / total_invested) * 100 if total_invested > 0 else 0

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Invested", f"${total_invested:,.2f}")
        m2.metric("Market Value", f"${total_value:,.2f}")
        m3.metric("Net Profit", f"${total_profit:,.2f}", delta=f"{profit_pct:.2f}%")

        # --- UPDATED HOLDINGS TABLE (WITH BUY DATE) ---
        st.markdown("### 📋 Active Holdings")
        
        # Select and reorder columns to include Date
        display_df = portfolio_df[[
            "Crypto", "Quantity", "Amount", "Buy Price", "Date", "Current Price", "Current Value", "Profit ($)"
        ]].copy()
        
        # Rename 'Amount' for clarity
        display_df.rename(columns={"Amount": "Invested ($)", "Date": "Buy Date"}, inplace=True)

        st.dataframe(
            display_df.style.format({
                "Quantity": "{:.6f}",
                "Invested ($)": "${:,.2f}",
                "Buy Price": "${:,.2f}",
                "Current Price": "${:,.2f}",
                "Current Value": "${:,.2f}",
                "Profit ($)": "${:,.2f}",
                "Buy Date": lambda x: x.strftime('%Y-%m-%d') # Format date for clean display
            }).map(lambda x: 'color: #00ffcc;' if (isinstance(x, (int, float)) and x > 0) else 'color: #ff4b4b;' if (isinstance(x, (int, float)) and x < 0) else '', subset=['Profit ($)']),
            use_container_width=True,
            hide_index=True
        )

        # --- CHARTS ---
        c1, c2 = st.columns(2)
        with c1:
            fig1 = px.pie(portfolio_df, names="Crypto", values="Current Value", title="Asset Allocation", hole=0.4, template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            fig2 = px.bar(portfolio_df, x="Crypto", y="Profit ($)", color="Profit ($)", title="Profit/Loss by Asset", template="plotly_dark", color_continuous_scale="RdYlGn")
            st.plotly_chart(fig2, use_container_width=True)

    # ==========================================
    # 🛒 2. TRANSACTION INTERFACE (BOTTOM SECTION)
    # ==========================================
    st.markdown("---")
    st.markdown("### ➕ / ➖ New Transaction")
    
    with st.container(border=True):
        t_col1, t_col2, t_col3, t_col4 = st.columns([1, 2, 2, 2])
        
        action = t_col1.radio("Action", ["Buy", "Sell"])
        coin = t_col2.selectbox("Crypto", sorted(df["Crypto"].unique()))
        amount = t_col3.number_input("Amount ($)", min_value=0.0, step=10.0)
        date = t_col4.date_input("Transaction Date")

        if st.button("Confirm Order", use_container_width=True):
            if amount > 0:
                if action == "Buy":
                    add_holding(email, coin, amount, str(date))
                    st.success(f"Added ${amount:,.2f} of {coin}!")
                else:
                    # Basic Sell Logic
                    sell_holding(email, coin, amount, str(date))
                    st.warning(f"Sold ${amount:,.2f} of {coin}!")
                st.rerun()
            else:
                st.error("Please enter an amount.")
