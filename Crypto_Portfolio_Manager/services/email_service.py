import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_USER, EMAIL_PASS

# ======================================================
# 🚀 CORE EMAIL ENGINE
# ======================================================
def send_email(to_email: str, subject: str, html_content: str):
    """
    Base engine to send HTML emails via Gmail SMTP.
    Requires a Google App Password (16 characters) to work.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = f"CryptoPort AI <{EMAIL_USER}>"
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(html_content, "html"))

        # Connection to Google SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        print(f"CRITICAL EMAIL ERROR: {e}")
        return False

# =========================
# WELCOME EMAIL
# =========================
def send_welcome_email(to_email: str):

    subject = "🎉 Welcome to Crypto SaaS Platform"

    html = f"""
    <html>
    <body style="font-family:Arial;background:#0f0c29;color:white;padding:20px;">
        <h2 style="color:#4cc9f0;">🚀 Welcome to Crypto SaaS</h2>
        <p>Your account has been successfully created.</p>
        
        <div style="background:#302b63;padding:15px;border-radius:10px;">
            <p>✔ Track your portfolio</p>
            <p>✔ AI-based insights</p>
            <p>✔ Real-time crypto prices</p>
        </div>

        <p style="margin-top:20px;">Happy Investing 💰</p>
    </body>
    </html>
    """

    return send_email(to_email, subject, html)
# ======================================================
# 🔐 2. OTP / LOGIN VERIFICATION
# ======================================================
def send_otp_email(to_email, otp_code):
    subject = f"🔐 {otp_code} is your Verification Code"
    html = f"""
    <div style="font-family: sans-serif; background-color: #0f0c29; color: white; padding: 40px; border-radius: 15px; text-align: center;">
        <h2 style="color: #00ffcc;">Security Code</h2>
        <p>Enter the code below to complete your login:</p>
        <div style="background: #1a1a3a; padding: 20px; font-size: 32px; font-weight: bold; letter-spacing: 10px; border: 1px solid #00ffcc; display: inline-block; margin: 20px 0;">
            {otp_code}
        </div>
        <p style="color: #ff4b4b; font-size: 14px;">This code expires in 10 minutes.</p>
    </div>
    """
    return send_email(to_email, subject, html)

# ======================================================
# ✅ 3. TRANSACTION NOTIFICATION (BUY/SELL RECEIPT)
# ======================================================
def send_transaction_notification(to_email, coin, action, amount):
    subject = f"✅ Transaction Confirmed: {action} {coin}"
    accent_color = "#00ffcc" if action == "Buy" else "#ff4b4b"
    
    html = f"""
    <div style="font-family: sans-serif; background-color: #0f0c29; color: white; padding: 25px; border-radius: 12px; border-left: 6px solid {accent_color};">
        <h3 style="color: {accent_color}; margin-top: 0;">{action} Order Settled</h3>
        <table style="width: 100%; color: white;">
            <tr><td><b>Asset:</b></td><td style="text-align: right;">{coin}</td></tr>
            <tr><td><b>Amount:</b></td><td style="text-align: right;">${amount:,.2f}</td></tr>
            <tr><td><b>Status:</b></td><td style="text-align: right; color: #00ffcc;">SUCCESS</td></tr>
        </table>
        <p style="font-size: 12px; color: #94A3B8; margin-top: 20px;">Your weighted average price has been updated.</p>
    </div>
    """
    return send_email(to_email, subject, html)

# ======================================================
# 📊 4. PORTFOLIO SUMMARY STATEMENT
# ======================================================
def send_portfolio_summary_email(to_email, portfolio_df):
    subject = "📊 Your Portfolio Performance Update"
    
    total_invested = portfolio_df["Total Invested"].sum()
    total_value = portfolio_df["Current Value"].sum()
    total_profit = total_value - total_invested
    
    rows = ""
    for _, row in portfolio_df.iterrows():
        p_color = "#00ffcc" if row["P/L ($)"] >= 0 else "#ff4b4b"
        rows += f"""
        <tr style="border-bottom: 1px solid #302b63;">
            <td style="padding: 10px;">{row['Asset']}</td>
            <td style="padding: 10px; text-align: right;">${row['Current Value']:,.2f}</td>
            <td style="padding: 10px; text-align: right; color: {p_color};">{row['ROI (%)']:.2f}%</td>
        </tr>
        """

    html = f"""
    <div style="font-family: sans-serif; background-color: #0f0c29; color: white; padding: 20px;">
        <h2 style="color: #00ffcc;">Portfolio Summary</h2>
        <div style="background: #1a1a3a; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <p>Total Value: <b style="color: #00ffcc; font-size: 20px;">${total_value:,.2f}</b></p>
            <p>Net P/L: <b style="color: {'#00ffcc' if total_profit >= 0 else '#ff4b4b'};">${total_profit:,.2f}</b></p>
        </div>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background: #302b63; color: #94A3B8;">
                <th style="padding: 10px; text-align: left;">Asset</th>
                <th style="padding: 10px; text-align: right;">Value</th>
                <th style="padding: 10px; text-align: right;">ROI</th>
            </tr>
            {rows}
        </table>
    </div>
    """
    return send_email(to_email, subject, html)

# ======================================================
# 🚨 5. PRICE ALERT NOTIFICATION
# ======================================================
def send_alert_email(to_email, coin, condition, target_price, current_price):
    subject = f"🚨 Price Alert: {coin} Target Hit!"
    color = "#00ffcc" if condition == "above" else "#ff4b4b"

    html = f"""
    <div style="font-family: sans-serif; background-color: #0f0c29; color: white; padding: 30px; border-radius: 15px; border: 2px solid {color};">
        <h2 style="color: {color};">Target Triggered!</h2>
        <p>Your alert for <b>{coin}</b> has been activated.</p>
        <p>Market Condition: Price is <b>{condition} ${target_price:,.2f}</b></p>
        <p style="font-size: 24px; font-weight: bold;">Current Price: ${current_price:,.2f}</p>
    </div>
    """
    return send_email(to_email, subject, html)
