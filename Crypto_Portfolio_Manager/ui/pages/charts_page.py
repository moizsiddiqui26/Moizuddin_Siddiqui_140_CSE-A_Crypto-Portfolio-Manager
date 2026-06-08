import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

def render_advanced_charts(df): # FIX: Accepts 'df' to calculate stats
    st.markdown("# Chart")

    # 1. Beginner-Friendly Asset Selection
    symbol_map = {
        "Bitcoin (BTC)": "BINANCE:BTCUSDT",
        "Ethereum (ETH)": "BINANCE:ETHUSDT",
        "Solana (SOL)": "BINANCE:SOLUSDT",
        "Ripple (XRP)": "BINANCE:XRPUSDT"
    }
    
    selected_name = st.selectbox("Pick a Coin to Analyze", list(symbol_map.keys()))
    symbol = symbol_map[selected_name]
    
    # Extract the ticker (e.g., 'BTC') for filtering the dataframe
    coin_ticker = selected_name.split("(")[1].split(")")[0]

    # --- NEW: PAST PERFORMANCE SNAPSHOT ---
    st.subheader(f"🌟 {selected_name} Performance at a Glance")
    
    # Filter data for the selected coin
    coin_data = df[df["Crypto"] == coin_ticker].sort_values("Date")
    
    if not coin_data.empty:
        latest_price = float(coin_data.iloc[-1]["Close"])
        
        # Calculate growth over different time periods
        prev_24h = coin_data.iloc[-2]["Close"] if len(coin_data) > 1 else latest_price
        prev_7d = coin_data.iloc[-7]["Close"] if len(coin_data) > 7 else latest_price
        
        chg_24h = ((latest_price - prev_24h) / prev_24h) * 100
        chg_7d = ((latest_price - prev_7d) / prev_7d) * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${latest_price:,.2f}")
        col2.metric("Last 24 Hours", f"{chg_24h:+.2f}%", delta=f"{chg_24h:.2f}%")
        col3.metric("Last 7 Days", f"{chg_7d:+.2f}%", delta=f"{chg_7d:.2f}%")

        # Simplified "How is it doing?" guide
        if chg_7d > 5:
            st.success(f"🚀 **Growing Fast:** {coin_ticker} has strong momentum this week!")
        elif chg_7d < -5:
            st.error(f"📉 **Price Drop:** {coin_ticker} is currently in a 'dip' compared to last week.")
        else:
            st.info(f"⚖️ **Steady:** {coin_ticker} is holding a stable price right now.")
    
    st.markdown("---")

    # 2. Advanced TradingView Terminal
    st.subheader("🔍 Deep Dive: Interactive Chart")
    html_code = f"""
    <div class="tradingview-widget-container">
      <div id="tradingview_chart"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
          "width": "100%", "height": 500, "symbol": "{symbol}",
          "interval": "D", "timezone": "Etc/UTC", "theme": "dark",
          "style": "1", "locale": "en", "toolbar_bg": "#0B1020",
          "enable_publishing": false, "hide_side_toolbar": false,
          "allow_symbol_change": true, "container_id": "tradingview_chart"
      }});
      </script>
    </div>
    """
    components.html(html_code, height=520)

    # 3. New User Education Section
    st.markdown("---")
    st.markdown("### 📚 New User Guide: Reading the Chart")
    
    with st.expander("🕯️ What are these vertical bars (Candlesticks)?"):
        st.write("""
        Instead of a single line, professional traders use **Candlesticks**. They tell a story:
        - **Green Bar:** Buyers were in control. The price closed higher than it opened.
        - **Red Bar:** Sellers were in control. The price closed lower than it opened.
        - **The Thin Lines (Wicks):** These show the highest and lowest prices reached during that day.
        """)
        

    with st.expander("📉 High vs. Low Volatility (Risk)"):
        st.write("""
        When the bars are very tall and jump up and down, that is **High Volatility**. 
        - This is riskier but can lead to faster gains. 

        - When bars are short and move in a steady line, it is **Low Volatility** (More stable).
        """)
