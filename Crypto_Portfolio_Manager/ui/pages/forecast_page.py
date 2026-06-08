import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from services.forecast_engine import get_forecast_summary

def render_forecast(df):
    # --- 1. SELECTION SECTION ---
    st.markdown("# 🔮 Price Prediction")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        st.markdown("### Select Asset to Analyze")
        coin = st.selectbox("", sorted(df["Crypto"].unique()), label_visibility="collapsed")
    with col_sel2:
        st.markdown("###  Investment ($)")
        amount = st.number_input("", value=1000.0, label_visibility="collapsed")

    # Process data for the specific coin
    coin_df = df[df["Crypto"] == coin].copy()
    coin_df['Date'] = pd.to_datetime(coin_df['Date']).dt.normalize()
    coin_df = coin_df.groupby('Date')['Close'].mean().reset_index().sort_values("Date")
    
    if len(coin_df) < 14:
        st.warning("⚠️ Insufficient historical data for this asset.")
        return

    # --- 2. FUTURE FORECAST RESULTS ---
    st.markdown("---")
    st.markdown("### 🚀 Future Forecast (Next 7 Days)")
    
    result = get_forecast_summary(coin_df, amount, 7)
    
    f1, f2, f3 = st.columns(3)
    f1.metric("Target Price", f"${result['predicted_price']:.2f}")
    f2.metric("Portfolio Goal", f"${result['expected_value']:.2f}")
    f3.metric("Growth Potential", f"{result['profit_pct']:.2f}%", delta=f"{result['profit_pct']:.2f}%")

    # --- 3. NEW USER TIPS (Beginner's Explanation) ---
    st.markdown("### 📝 What do these numbers mean?")
    
    with st.expander("🔍 Click here to see the Beginner's Explanation"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**What is ROI?**")
            st.write("""
            ROI stands for **Return on Investment**. 
            - If it's **+5%**, your $1,000 becomes $1,050.
            - If it's **-5%**, your $1,000 becomes $950.
            """)
        with col_b:
            st.write("**How accurate is this?**")
            st.write("""
            Predictions are based on **Historical Trends**. If the market changes suddenly due to news or global events, the AI may not be 100% accurate. 
            """)

        st.info("💡 **Pro Tip:** Don't put all your money in one coin. Use the 'Risk' page to see which coins are the safest!")

    # --- 4. AI PERFORMANCE REVIEW (Backtesting Last 7 Days) ---
    st.markdown("---")
    st.markdown("### Performance Review (Last 7 Working Days)")
    
    train_data = coin_df.iloc[:-7].reset_index(drop=True)
    actual_last_7 = coin_df.iloc[-7:].reset_index(drop=True)
    
    X_train = np.arange(len(train_data)).reshape(-1, 1)
    y_train = train_data["Close"]
    model = LinearRegression().fit(X_train, y_train)
    
    X_test = np.arange(len(train_data), len(train_data) + 7).reshape(-1, 1)
    predicted_last_7 = model.predict(X_test)

    comparison_df = pd.DataFrame({
        "Date": actual_last_7["Date"].dt.strftime('%Y-%m-%d'),
        "Actual Price": actual_last_7["Close"].values,
        "AI Prediction": predicted_last_7,
    })
    
    comparison_df["Difference (%)"] = ((comparison_df["AI Prediction"] - comparison_df["Actual Price"]) / comparison_df["Actual Price"]) * 100
    
    def style_diff(val):
        color = '#ff4b4b' if abs(val) > 5 else '#00ffcc'
        return f'color: {color}; font-weight: bold;'

    styled_table = comparison_df.style.format({
        "Actual Price": "${:,.2f}",
        "AI Prediction": "${:,.2f}",
        "Difference (%)": "{:,.2f}%"
    }).map(style_diff, subset=['Difference (%)'])

    st.table(styled_table)

    # --- 5. FIXED ACCURACY METRICS ---
    # 1. Calculate Average Deviation
    avg_err_val = comparison_df["Difference (%)"].abs().mean()
    
    # 2. Calculate R2 Score (Trend Strength)
    r2_val = r2_score(actual_last_7["Close"], predicted_last_7)
    
    # 3. Calculate Directional Accuracy
    correct_dir = 0
    for i in range(1, len(comparison_df)):
        act_up = actual_last_7["Close"].iloc[i] > actual_last_7["Close"].iloc[i-1]
        pred_up = predicted_last_7[i] > predicted_last_7[i-1]
        if act_up == pred_up: correct_dir += 1
    dir_acc_val = int((correct_dir / 6) * 100)

    # Display Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Avg. Deviation", f"{avg_err_val:.2f}%", 
              help="Lower is better. Shows average gap between AI and Truth.")
    
    
    m3.metric("Directional Accuracy", f"{dir_acc_val}%", 
              help="How often the AI correctly guessed 'Up' vs 'Down'.")
