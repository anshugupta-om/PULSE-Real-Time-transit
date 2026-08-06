# auth_manager.py - Dual Portal Auth Engine with Master System Audit CSV Sync

import sqlite3
import time
import random
import bcrypt
import os
import pandas as pd
import streamlit as st
from datetime import datetime
from db_manager import log_login_event, MASTER_AUDIT_CSV, init_master_csv

DB_NAME = 'pulse_auth.db'
USER_REGISTRY_CSV = 'registered_users_registry.csv'

# ---------------------------------------------------------
# 1. DATABASE INITIALIZATION & CSV SYNC
# ---------------------------------------------------------
def init_auth_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  password_hash TEXT, 
                  role TEXT,
                  full_name TEXT,
                  email TEXT,
                  mobile TEXT,
                  reg_time TEXT)''')
    
    c.execute("SELECT * FROM users WHERE username='anshu'")
    if not c.fetchone():
        admin_pass_bytes = '1234'.encode('utf-8')
        hashed_pwd = bcrypt.hashpw(admin_pass_bytes, bcrypt.gensalt()).decode('utf-8')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO users (username, password_hash, role, full_name, email, mobile, reg_time) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                  ('anshu', hashed_pwd, 'admin', 'Chief Admin Anshu', 'admin@pulse.gov.in', '9999999999', current_time))
    
    conn.commit()
    conn.close()
    sync_registered_users_csv()
    init_master_csv()

def sync_registered_users_csv():
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT username AS 'Username', full_name AS 'Full Name', email AS 'Email Address', mobile AS 'Mobile No', role AS 'User Role', reg_time AS 'Registration Timestamp' FROM users", conn)
        conn.close()
        df.to_csv(USER_REGISTRY_CSV, index=False)
        return df
    except Exception:
        return pd.DataFrame()

# ---------------------------------------------------------
# 2. SECURITY HELPER FUNCTIONS
# ---------------------------------------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        if stored_hash.startswith('$2b$') or stored_hash.startswith('$2a$'):
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        else:
            from werkzeug.security import check_password_hash
            return check_password_hash(stored_hash, password)
    except Exception:
        return False

def check_rate_limit(identity: str) -> bool:
    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = {}
    
    record = st.session_state.failed_attempts.get(identity, {"count": 0, "lock_until": 0})
    if record["count"] >= 3:
        time_remaining = int(60 - (time.time() - record["lock_until"]))
        if time_remaining > 0:
            st.error(f"🚨 Account locked for security. Try again in {time_remaining} seconds.")
            return False
        else:
            st.session_state.failed_attempts[identity] = {"count": 0, "lock_until": 0}
    return True

def record_failed_attempt(identity: str):
    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = {}
        
    record = st.session_state.failed_attempts.get(identity, {"count": 0, "lock_until": 0})
    record["count"] += 1
    if record["count"] >= 3:
        record["lock_until"] = time.time()
    st.session_state.failed_attempts[identity] = record

# ---------------------------------------------------------
# 3. ANIMATED METRO BACKGROUND & CUSTOM CSS
# ---------------------------------------------------------
def inject_metro_auth_css():
    st.markdown("""
    <style>
    @keyframes moveTrainBg {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(rgba(15, 23, 42, 0.70), rgba(15, 23, 42, 0.85)),
                    url('https://images.unsplash.com/photo-1542296332-2e4473faf563?q=80&w=1920') repeat-x center center fixed;
        background-size: cover;
        animation: moveTrainBg 35s ease infinite;
    }
    
    @keyframes pulseGlow {
        0% { text-shadow: 0 0 10px #00e5ff, 0 0 20px #00e5ff, 0 0 30px #3b82f6; }
        50% { text-shadow: 0 0 20px #00e5ff, 0 0 35px #00e5ff, 0 0 50px #3b82f6; }
        100% { text-shadow: 0 0 10px #00e5ff, 0 0 20px #00e5ff, 0 0 30px #3b82f6; }
    }

    .pulse-animated-title {
        font-size: 38px;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        letter-spacing: 2px;
        animation: pulseGlow 2.5s infinite alternate;
        margin-bottom: 2px;
    }

    div[data-testid="stVerticalBlock"] > div:has(div.stTabs) {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.9) !important;
    }

    .otp-banner {
        background: linear-gradient(90deg, rgba(0,229,255,0.2) 0%, rgba(59,130,246,0.2) 100%);
        border: 1px solid #00e5ff;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 15px;
        color: #ffffff;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 0 15px rgba(0,229,255,0.3);
    }
    .otp-code {
        font-size: 22px;
        font-weight: 800;
        color: #00e5ff;
        letter-spacing: 4px;
        background: rgba(0,0,0,0.4);
        padding: 2px 10px;
        border-radius: 6px;
    }

    .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #00e5ff 0%, #3b82f6 100%) !important;
        color: #020617 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }

    .user-registry-box {
        background: rgba(6, 182, 212, 0.08);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 16px;
        padding: 20px;
        margin-top: 25px;
        box-shadow: 0 10px 30px rgba(0, 229, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. ADMIN DASHBOARD REGISTRATION & MASTER LOGS RENDERER
# ---------------------------------------------------------
def render_admin_user_registry():
    """Displays Full Unclipped System Master Activity CSV Table on Admin Portal"""
    st.markdown("---")
    st.markdown("""
    <div class="user-registry-box">
        <h3 style="color: #00e5ff; margin-bottom: 5px;">📊 Master Unified Activity Audit Logs (Live CSV)</h3>
        <p style="color: #94a3b8; font-size: 14px;">Complete administrative records tracking User Logins, Journeys (Source -> Destination), Chatbot usage, and System Queries.</p>
    </div>
    """, unsafe_allow_html=True)
    
    init_master_csv()
    if os.path.exists(MASTER_AUDIT_CSV):
        df_audit = pd.read_csv(MASTER_AUDIT_CSV)
        if not df_audit.empty:
            # Full Width Unclipped DataFrame Rendering
            st.dataframe(df_audit, use_container_width=True)
            
            csv_data = df_audit.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Complete Master Audit Logs (CSV)",
                data=csv_data,
                file_name=MASTER_AUDIT_CSV,
                mime='text/csv',
                use_container_width=True
            )
        else:
            st.info("No activity logged yet.")

# ---------------------------------------------------------
# 5. MAIN DUAL PORTAL AUTHENTICATION PAGE
# ---------------------------------------------------------
def login_page():
    init_auth_db()
    inject_metro_auth_css()
    
    st.markdown("<div class='pulse-animated-title'>🚆 Welcome to PULSE</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-sub'>Govt. Authorized Live Transit Navigator (Enterprise Portal)</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        tab1, tab2 = st.tabs(["👥 Commuter Portal", "🛡️ Authority Portal"])
        
        with tab1:
            auth_mode = st.radio("Select Action:", ["Login", "New Commuter Registration", "Forgot Password?"], horizontal=True)
            
            if auth_mode == "New Commuter Registration":
                st.info("📝 Create New Commuter Account")
                full_name = st.text_input("Full Name:", placeholder="e.g. Passenger XYZ")
                mobile = st.text_input("Mobile Number (10 digits):", max_chars=10, placeholder="9876543210")
                email = st.text_input("Email Address:", placeholder="passenger@example.com")
                st.markdown("---")
                user_name = st.text_input("Choose Username:")
                user_pass = st.text_input("Create Password (min 6 chars):", type="password")
                
                if st.button("Submit Registration ➔", use_container_width=True):
                    if full_name and mobile and email and user_name and user_pass:
                        if len(mobile) == 10 and mobile.isdigit():
                            if len(user_pass) < 6:
                                st.error("⚠️ Password must be at least 6 characters long.")
                            else:
                                conn = sqlite3.connect(DB_NAME)
                                c = conn.cursor()
                                c.execute("SELECT * FROM users WHERE username=?", (user_name.lower(),))
                                if c.fetchone():
                                    st.warning("⚠️ Username already exists.")
                                else:
                                    hashed_pwd = hash_password(user_pass)
                                    reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    c.execute("INSERT INTO users (username, password_hash, role, full_name, email, mobile, reg_time) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                                              (user_name.lower(), hashed_pwd, 'user', full_name.title(), email.lower(), mobile, reg_time))
                                    conn.commit()
                                    conn.close()
                                    
                                    sync_registered_users_csv()
                                    st.success("✅ Account created & CSV synced! Switch to 'Login'.")
                                conn.close()
                        else:
                            st.error("⚠️ Enter valid 10-digit mobile number.")
                    else:
                        st.warning("⚠️ All fields are mandatory.")
                        
            elif auth_mode == "Login":
                user_name = st.text_input("Username / Email:", placeholder="e.g. Passenger XYZ")
                user_pass = st.text_input("Password:", type="password")
                
                if st.button("Proceed to MFA Check ➔", use_container_width=True):
                    if user_name and user_pass:
                        if check_rate_limit(user_name.lower()):
                            conn = sqlite3.connect(DB_NAME)
                            c = conn.cursor()
                            c.execute("SELECT password_hash, role, full_name, username FROM users WHERE (username=? OR email=?) AND role='user'", (user_name.lower(), user_name.lower()))
                            result = c.fetchone()
                            conn.close()
                            
                            if result and verify_password(user_pass, result[0]):
                                otp = str(random.randint(100000, 999999))
                                st.session_state.pending_auth = {
                                    "username": result[3],
                                    "full_name": result[2],
                                    "role": "user",
                                    "otp": otp,
                                    "time": time.time()
                                }
                            else:
                                record_failed_attempt(user_name.lower())
                                st.error("❌ Invalid Credentials. Check username or password.")
                    else:
                        st.warning("Please enter your credentials.")

                if "pending_auth" in st.session_state and st.session_state.pending_auth.get("role") == "user":
                    elapsed = time.time() - st.session_state.pending_auth.get("time", 0)
                    
                    if elapsed <= 20:
                        st.markdown(f"""
                        <div class="otp-banner">
                            📲 <b>Multi-Factor Authentication Code:</b> <span class="otp-code">{st.session_state.pending_auth.get('otp')}</span>
                            <br><small style="color:#94a3b8;">Code expires in {int(20 - elapsed)} seconds...</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        mfa_code = st.text_input("Enter 6-Digit Code shown above:", max_chars=6)
                        
                        if st.button("VERIFY & ACCESS DASHBOARD", type="primary", use_container_width=True):
                            if mfa_code == st.session_state.pending_auth.get("otp"):
                                st.session_state.logged_in = True
                                st.session_state.username = st.session_state.pending_auth["username"]
                                st.session_state.role = "user"
                                
                                # Log Login Event to Master CSV
                                log_login_event(st.session_state.username, "user")
                                
                                del st.session_state.pending_auth
                                st.success(f"Welcome back, {st.session_state.username}! Redirecting...")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("❌ Incorrect MFA Code.")
                    else:
                        del st.session_state.pending_auth
                        st.warning("⏱️ MFA Code expired! Click 'Proceed to MFA Check' again.")

            elif auth_mode == "Forgot Password?":
                st.info("🔑 Secure Password Recovery Flow")
                rec_email = st.text_input("Registered Email Address:", placeholder="passenger@example.com")
                rec_mobile = st.text_input("Registered Mobile Number:", max_chars=10)
                new_pass = st.text_input("New Password:", type="password")
                
                if st.button("Reset Password ➔", use_container_width=True):
                    if rec_email and rec_mobile and new_pass:
                        conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        c.execute("SELECT username FROM users WHERE email=? AND mobile=?", (rec_email.lower(), rec_mobile))
                        user_found = c.fetchone()
                        
                        if user_found:
                            new_hash = hash_password(new_pass)
                            c.execute("UPDATE users SET password_hash=? WHERE username=?", (new_hash, user_found[0]))
                            conn.commit()
                            conn.close()
                            sync_registered_users_csv()
                            st.success("✅ Password reset successfully!")
                        else:
                            st.error("❌ Verification failed.")
                            conn.close()

        with tab2:
            st.caption("🔒 Authorized Railway Police & Admin Portal")
            admin_user = st.text_input("Admin Username", placeholder="e.g. anshu")
            admin_pass = st.text_input("Admin Password", type="password")
            
            if st.button("Login as Authority ➔", use_container_width=True):
                if admin_user and admin_pass:
                    if check_rate_limit(admin_user.lower()):
                        conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        c.execute("SELECT password_hash, role, full_name, username FROM users WHERE username=? AND role='admin'", (admin_user.lower(),))
                        result = c.fetchone()
                        conn.close()
                        
                        if result and verify_password(admin_pass, result[0]):
                            otp = str(random.randint(100000, 999999))
                            st.session_state.pending_auth = {
                                "username": result[3],
                                "full_name": result[2],
                                "role": "admin",
                                "otp": otp,
                                "time": time.time()
                            }
                        else:
                            record_failed_attempt(admin_user.lower())
                            st.error("❌ Invalid Admin Credentials.")
                else:
                    st.warning("Please enter admin credentials.")

            if "pending_auth" in st.session_state and st.session_state.pending_auth.get("role") == "admin":
                elapsed = time.time() - st.session_state.pending_auth.get("time", 0)
                
                if elapsed <= 20:
                    st.markdown(f"""
                    <div class="otp-banner" style="border-color: #ff1744;">
                        🛡️ <b>Authority Security Code:</b> <span class="otp-code" style="color: #ff1744;">{st.session_state.pending_auth.get('otp')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    admin_mfa = st.text_input("Enter 6-Digit Authority Code:", max_chars=6)
                    
                    if st.button("AUTHENTICATE ADMIN SESSION", type="primary", use_container_width=True):
                        if admin_mfa == st.session_state.pending_auth.get("otp"):
                            st.session_state.logged_in = True
                            st.session_state.username = st.session_state.pending_auth["username"]
                            st.session_state.role = "admin"
                            
                            # Log Admin Login
                            log_login_event(st.session_state.username, "admin")
                            
                            del st.session_state.pending_auth
                            st.success("Admin Portal Unlocked! Redirecting...")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("❌ Incorrect Security Code.")
                else:
                    del st.session_state.pending_auth
                    st.warning("⏱️ Security Passcode expired!")