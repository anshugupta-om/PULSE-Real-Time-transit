# auth_manager.py - Dual Portal Authentication Engine

import sqlite3
import time
import streamlit as st
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = 'pulse_auth.db'

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
        hashed_pwd = generate_password_hash('1234')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO users (username, password_hash, role, full_name, email, mobile, reg_time) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                  ('anshu', hashed_pwd, 'admin', 'Chief Admin Anshu', 'admin@pulse.gov.in', '9999999999', current_time))
    
    conn.commit()
    conn.close()

def login_page():
    st.markdown("<h1 style='text-align: center;'>🚆 Welcome to PULSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Govt. Authorized Live Transit Navigator (Secure Portal)</p><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs([" Commuter (Public)", " Authority Portal"])
        
        with tab1:
            auth_mode = st.radio("Select Action:", ["Login", "New Commuter Registration"], horizontal=True)
            
            if auth_mode == "New Commuter Registration":
                st.info(" Commuter Registration")
                full_name = st.text_input("Full Name :")
                mobile = st.text_input("Mobile Number (10 digits):", max_chars=10)
                email = st.text_input("Email Address:")
                st.markdown("---")
                user_name = st.text_input("Choose a Username:")
                user_pass = st.text_input("Create Password:", type="password")
                
                if st.button("Submit Registration ", use_container_width=True):
                    if full_name and mobile and email and user_name and user_pass:
                        if len(mobile) == 10 and mobile.isdigit():
                            conn = sqlite3.connect(DB_NAME)
                            c = conn.cursor()
                            c.execute("SELECT * FROM users WHERE username=?", (user_name.lower(),))
                            if c.fetchone():
                                st.warning("⚠️ Username already exists.")
                            else:
                                hashed_pwd = generate_password_hash(user_pass)
                                reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                c.execute("INSERT INTO users (username, password_hash, role, full_name, email, mobile, reg_time) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                                          (user_name.lower(), hashed_pwd, 'user', full_name.title(), email.lower(), mobile, reg_time))
                                conn.commit()
                                st.success("✅ Registration successful! Please switch to 'Login'.")
                            conn.close()
                        else:
                            st.error("⚠️ Enter valid 10-digit mobile number.")
                    else:
                        st.warning("⚠️ All fields are mandatory.")
                        
            elif auth_mode == "Login":
                user_name = st.text_input("Username:")
                user_pass = st.text_input("Password:", type="password")
                if st.button("Login ", use_container_width=True):
                    if user_name and user_pass:
                        conn = sqlite3.connect(DB_NAME)
                        c = conn.cursor()
                        c.execute("SELECT password_hash, role, full_name FROM users WHERE username=? AND role='user'", (user_name.lower(),))
                        result = c.fetchone()
                        conn.close()
                        
                        if result and check_password_hash(result[0], user_pass):
                            st.session_state.logged_in = True
                            st.session_state.username = result[2]
                            st.session_state.role = "user"
                            st.success(f"Welcome back, {result[2]}! Redirecting...")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Invalid Credentials.")
                    else:
                        st.warning("Please enter credentials.")

        with tab2:
            st.markdown("For Railway Police & Authorities Only.")
            admin_user = st.text_input("Admin Username")
            admin_pass = st.text_input("Admin Password", type="password")
            
            if st.button("Login as Authority ", use_container_width=True):
                if admin_user and admin_pass:
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute("SELECT password_hash, role, full_name FROM users WHERE username=? AND role='admin'", (admin_user.lower(),))
                    result = c.fetchone()
                    conn.close()
                    
                    if result and check_password_hash(result[0], admin_pass):
                        st.session_state.logged_in = True
                        st.session_state.username = "Authority: " + result[2]
                        st.session_state.role = "admin"
                        st.success("Login Successful! Redirecting...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid Admin Credentials.")
                else:
                    st.warning("Please enter credentials.")