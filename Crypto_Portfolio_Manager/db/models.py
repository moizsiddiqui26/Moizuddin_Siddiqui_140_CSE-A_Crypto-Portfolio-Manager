# db/models.py

from db.database import get_connection
import sqlite3

# ======================================================
# 👤 USER MODELS (Authentication & Security)
# ======================================================

def create_user(name, email, password):
    """Registers a new user in the system."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Returns False if the email already exists
        return False
    finally:
        conn.close()

def fetch_user(email):
    """Retrieves user details for login verification."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    conn.close()
    return user

def update_user_password(email, password):
    """Updates password for the Forgot Password flow."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET password=? WHERE email=?",
        (password, email)
    )
    conn.commit()
    conn.close()


# ======================================================
# 💼 PORTFOLIO MODELS (The Buy/Sell Logic)
# ======================================================

def add_holding(email, crypto, amount, date):
    """Records a BUY transaction (Positive value)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO holdings (email, crypto, amount, date) VALUES (?, ?, ?, ?)",
        (email, crypto, abs(amount), date)
    )
    conn.commit()
    conn.close()

def sell_holding(email, crypto, amount, date):
    """
    Records a SELL transaction (Negative value).
    This allows us to use SUM(amount) in the UI to find the current balance.
    """
    conn = get_connection()
    cur = conn.cursor()
    # Force negative value for sells
    cur.execute(
        "INSERT INTO holdings (email, crypto, amount, date) VALUES (?, ?, ?, ?)",
        (email, crypto, -abs(amount), date)
    )
    conn.commit()
    conn.close()

def get_holdings(email):
    """Retrieves the full transaction history for a user's portfolio."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT crypto, amount, date FROM holdings WHERE email=? ORDER BY date ASC",
        (email,)
    )
    data = cur.fetchall()
    conn.close()
    return data


# ======================================================
# 🚨 ALERT MODELS (Price Monitoring)
# ======================================================

def add_alert(email, coin, condition, target_price):
    """Saves a user-defined price alert."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO alerts (email, coin, condition, target_price, active)
        VALUES (?, ?, ?, ?, 1)
    """, (email, coin, condition, target_price))
    conn.commit()
    conn.close()

def get_alerts(email):
    """Fetches all alerts for a specific user to display in the UI."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, coin, condition, target_price, active
        FROM alerts WHERE email = ?
    """, (email,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_active_alerts():
    """System-level function to fetch all alerts that need checking."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, email, coin, condition, target_price
        FROM alerts WHERE active = 1
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def deactivate_alert(alert_id):
    """Disables an alert once it has been triggered and sent via email."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE alerts SET active = 0 WHERE id = ?", (alert_id,))
    conn.commit()
    conn.close()
