import streamlit as st
from datetime import datetime
import time
import random
import folium
from streamlit_folium import st_folium
import hashlib
import os
import sqlite3
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

from chatbot_engine import pulse_chatbot

# --- CUSTOM MODULES ---
try:
    from ai_predictor import predict_crowd_density
    from db_manager import log_journey_sql, get_admin_dataframe, clear_all_data, get_next_journey_id
    from womens_safety import get_womens_helpline, trigger_sos_alert
    from accident_prevention import get_station_hazard, check_deboarding_risk
    MODULES_LOADED = True
except ImportError as e:
    st.error(f"⚠️ Missing Module: {e}. Please make sure all 5 new python files are in the same folder.")
    MODULES_LOADED = False

# --- CONFIGURATION & SETUP ---
st.set_page_config(page_title="PULSE - Live Mumbai Navigator", layout="wide")

# ==========================================
#  SECURE DATABASE SETUP 

def init_auth_db():
    conn = sqlite3.connect('pulse_auth.db')
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

init_auth_db()

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'role' not in st.session_state:
    st.session_state.role = None
if 'tracking' not in st.session_state:
    st.session_state.tracking = False
if 'journey_id' not in st.session_state:
    st.session_state.journey_id = None 
if 'reached' not in st.session_state:
    st.session_state.reached = False
if 'original_eta_mins' not in st.session_state:
    st.session_state.original_eta_mins = 0
if 'current_live_eta' not in st.session_state:
    st.session_state.current_live_eta = 0
if 'previous_eta' not in st.session_state:
    st.session_state.previous_eta = 0

# --- DATA: DICTIONARIES & COORDINATES ---
LANGUAGES = {
    "English": {
        "title": "🚆 PULSE: Real-Time Transit Navigator",
        "subtitle": "Search locations, track live routes, check crowd density, and get smart alerts.",
        "line": "Select Line",
        "from": "📍 From",
        "to": "🏁 To",
        "monsoon": "🌧️ Is it Raining? (Monsoon Mode)",
        "start": "Start Live Tracking 🚀",
        "same_loc": "Source and Destination cannot be the same!",
        "tracking_msg": "🟢 Tracking:",
        "dashboard": "### 📡 Live Status Dashboard",
        "map_title": "### 🗺️ Live Route Map",
        "orig_eta": "Original ETA",
        "live_eta": "Live ETA",
        "sync": "Last Data Sync",
        "insights": "#### 🚉 Transit Insights",
        "crowd": "AI Crowd Predictor",
        "next_train": "Next Train In",
        "weather": "Monsoon Impact",
        "completed": "🎉 Journey Completed!"
    },
    "Hindi": {
        "title": "🚆 पल्स (PULSE): लाइव ट्रांज़िट नेविगेटर",
        "subtitle": "लोकेशन खोजें, लाइव रूट ट्रैक करें, भीड़ की जानकारी लें और स्मार्ट अलर्ट पाएं।",
        "line": "रूट लाइन चुनें",
        "from": "📍 कहाँ से",
        "to": "🏁 कहाँ तक",
        "monsoon": "🌧️ क्या बारिश हो रही है? (मानसून मोड)",
        "start": "लाइव ट्रैकिंग शुरू करें 🚀",
        "same_loc": "शुरुआती और आखिरी लोकेशन एक नहीं हो सकती!",
        "tracking_msg": "🟢 ट्रैकिंग जारी:",
        "dashboard": "### 📡 लाइव स्टेटस डैशबोर्ड",
        "map_title": "### 🗺️ लाइव रूट मैप",
        "orig_eta": "मूल अनुमानित समय",
        "live_eta": "वर्तमान लाइव ETA",
        "sync": "आखिरी डेटा सिंक",
        "insights": "#### 🚉 ट्रांज़िट इनसाइट्स",
        "crowd": "AI भीड़ का अनुमान",
        "next_train": "अगली ट्रेन",
        "weather": "मौसम का असर",
        "completed": "🎉 यात्रा पूरी हुई!"
    },
    "Marathi": {
        "title": "🚆 पल्स (PULSE): थेट ट्रान्झिट नेव्हिगेटर",
        "subtitle": "लोकेशन शोधा, थेट मार्ग ट्रॅक करा, गर्दी तपासा आणि स्मार्ट अलर्ट मिळवा.",
        "line": "मार्ग लाइन निवडा",
        "from": "📍 कुठून",
        "to": "🏁 कुठे",
        "monsoon": "🌧️ पाऊस पडत आहे का? (पावसाळा मोड)",
        "start": "थेट ट्रॅकिंग सुरू करा 🚀",
        "same_loc": "सुरुवातीचे आणि अंतिम लोकेशन एकच असू शकत नाही!",
        "tracking_msg": "🟢 ट्रॅकिंग चालू:",
        "dashboard": "### 📡 थेट स्थिती डॅशबोर्ड",
        "map_title": "### 🗺️ थेट मार्ग नकाशा",
        "orig_eta": "मूळ अंदाजित वेळ",
        "live_eta": "सध्याची थेट ETA",
        "sync": "शेवटचा डेटा सिंक",
        "insights": "#### 🚉 ट्रान्झिट इनसाइट्स",
        "crowd": "AI गर्दीची घनता",
        "next_train": "पुढची ट्रेन",
        "weather": "हवामानाचा प्रभाव",
        "completed": "🎉 प्रवास पूर्ण झाला!"
    }
}
MUMBAI_LOCATIONS = ["Andheri East", "Andheri West", "Bandra Kurla Complex (BKC)", "Bandra West", "Borivali", "Churchgate", "CSMT", "Dadar", "Goregaon", "Kurla", "Lower Parel", "Marine Drive", "Thane"]

KNOWN_COORDS = {
    "Andheri East": [19.1136, 72.8697], "Bandra Kurla Complex (BKC)": [19.0653, 72.8656], 
    "Borivali": [19.2307, 72.8567], "Churchgate": [18.9322, 72.8264], 
    "Dadar": [19.0178, 72.8478], "Kurla": [19.0732, 72.8798], 
    "CSMT": [18.9400, 72.8353], "Thane": [19.2183, 72.9781]
}

def get_coordinates(loc_name):
    if loc_name in KNOWN_COORDS:
        return KNOWN_COORDS[loc_name]
    h = int(hashlib.md5(loc_name.encode()).hexdigest(), 16)
    return [19.0760 + (h%100 - 50)/1000.0, 72.8777 + (h%100 - 50)/1000.0]

# ==========================================
#  SECURE DUAL LOGIN PAGE 

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
                            conn = sqlite3.connect('pulse_auth.db')
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
                                st.success(f"✅ Registration successful! Please switch to 'Login'.")
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
                        conn = sqlite3.connect('pulse_auth.db')
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
                    conn = sqlite3.connect('pulse_auth.db')
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

# ==========================================
#  MAIN APP

def main_app():
    if not MODULES_LOADED:
        return

    def calculate_mock_base_eta(source, destination, is_monsoon):
        combined_name = source + destination
        hash_val = sum(ord(char) for char in combined_name)
        base_eta = (hash_val % 60) + 20 
        if is_monsoon:
            base_eta += random.randint(15, 30)
        return base_eta

    def get_fluctuated_eta(current_eta):
        fluctuation = random.choices([-2, 3, 5], weights=[30, 40, 30])[0]
        return max(1, current_eta + fluctuation)

    # --- SIDEBAR: SETTINGS & ADMIN PANEL ---
    st.sidebar.header("⚙️ Settings")
    selected_lang = st.sidebar.selectbox("Language / भाषा:", ["English", "Hindi", "Marathi"])
    t = LANGUAGES[selected_lang]
    st.sidebar.markdown("---")
    
    # 🛠️ ADMIN PANEL 
    if st.session_state.role == "admin":
        st.sidebar.header(" Authority Control Panel")
        
        # --- SECTION 1: LIVE JOURNEYS ---
        st.sidebar.subheader(" Live Journeys ")
        try:
            admin_df = get_admin_dataframe()
            if not admin_df.empty:
                sos_alerts = admin_df[admin_df['Status'] == "🚨 SOS EMERGENCY"]
                if not sos_alerts.empty:
                    st.sidebar.error("🚨 **ACTIVE SOS EMERGENCIES** 🚨")
                    for index, row in sos_alerts.head(3).iterrows():
                        st.sidebar.warning(f"👤 **User:** {row['User']}\n\n📍 **Location:** {row['From']} to {row['To']}\n\n🕒 **Time:** {row['Time']}")
                
                st.sidebar.dataframe(admin_df, use_container_width=True) 
                
                csv_journeys = admin_df.to_csv(index=False).encode('utf-8')
                st.sidebar.download_button(" Download Live Journeys Data", data=csv_journeys, file_name="pulse_journeys.csv", mime="text/csv", use_container_width=True, key="dl_journeys")
            else:
                st.sidebar.info("No active journeys.")
        except Exception as e:
            st.sidebar.error("Journey Database loading...")
            
        if st.sidebar.button("🗑️ Clear Journeys Data", type="primary", use_container_width=True, key="clr_journeys"):
            clear_all_data()
            st.sidebar.success("Journey Database Cleared! Refreshing...")
            time.sleep(1)
            st.rerun()

        st.sidebar.markdown("---")

        # --- SECTION 2: REGISTERED USERS  ---
        st.sidebar.subheader(" Registered Commuters")
        try:
            auth_conn = sqlite3.connect('pulse_auth.db')
            users_df = pd.read_sql_query("SELECT full_name as 'Full Name', username as 'Username', mobile as 'Mobile No.', email as 'Email', reg_time as 'Reg. Time' FROM users WHERE role='user' ORDER BY reg_time DESC", auth_conn)
            auth_conn.close()
            
            if not users_df.empty:
                st.sidebar.success(f"Total Registered Commuters: {len(users_df)}")
                st.sidebar.dataframe(users_df, use_container_width=True)
                
                csv_users = users_df.to_csv(index=False).encode('utf-8')
                st.sidebar.download_button("📥 Download Commuter Data", data=csv_users, file_name="pulse_commuters.csv", mime="text/csv", use_container_width=True, key="dl_users")
            else:
                st.sidebar.info("No commuters registered yet.")
        except Exception as e:
            st.sidebar.error("Commuter Database loading...")

        if st.sidebar.button("🗑️ Clear All Commuters (Reset)", type="primary", use_container_width=True, key="clr_users"):
            auth_conn = sqlite3.connect('pulse_auth.db')
            c = auth_conn.cursor()
            c.execute("DELETE FROM users WHERE role='user'") 
            auth_conn.commit()
            auth_conn.close()
            st.sidebar.success("Commuter Database Cleared! Refreshing...")
            time.sleep(1)
            st.rerun()

        st.sidebar.markdown("---")

    # LOGOUT BUTTON
    if st.sidebar.button("Logout 🚪", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    # --- UI: TITLES ---
    badge = " Admin" if st.session_state.role == "admin" else " Commuter"
    st.title(f" Welcome, {st.session_state.username}! ({badge})")
    st.markdown(f"### {t['title']}")

    # ==========================================
    # PHASE 1: ENTERING LOCATION & STARTING
    if not st.session_state.tracking:
        selected_line = st.selectbox(t["line"], ["Western Line", "Central Line", "Harbour Line"])
        
        col1, col2 = st.columns(2)
        with col1:
            source = st.selectbox(t["from"], MUMBAI_LOCATIONS, index=0)
        with col2:
            destination = st.selectbox(t["to"], MUMBAI_LOCATIONS, index=4)

        is_monsoon = st.checkbox(t["monsoon"])

        
        
        if st.button(t["start"]):
            if source == destination:
                st.warning(t["same_loc"])
            else:
                with st.spinner("Loading Map and Routes..."):
                    time.sleep(1)
                    initial_eta = calculate_mock_base_eta(source, destination, is_monsoon)
                    
                    st.session_state.journey_id = get_next_journey_id()
                    log_journey_sql(
                        st.session_state.journey_id, 
                        st.session_state.username, 
                        selected_line, 
                        source, 
                        destination, 
                        f"Started (ETA: {initial_eta}m)"
                    )
                    
                st.session_state.tracking = True
                st.session_state.reached = False
                st.session_state.original_eta_mins = initial_eta
                st.session_state.current_live_eta = initial_eta
                st.session_state.previous_eta = initial_eta
                st.session_state.source = source
                st.session_state.destination = destination
                st.session_state.monsoon_active = is_monsoon
                st.session_state.selected_line = selected_line
                st.rerun()
        # Integrating your Chatbot function
        pulse_chatbot()
    # ==========================================
    # PHASE 2: LIVE TRACKING, MAP & ALERTS
    else:
        st.success(f"{t['tracking_msg']} **{st.session_state.source}** ➡️ **{st.session_state.destination}** via **{st.session_state.selected_line}**")
        
        if st.checkbox("✅ I have reached my destination!"):
            st.session_state.tracking = False
            log_journey_sql(
                st.session_state.journey_id, 
                st.session_state.username, 
                st.session_state.selected_line, 
                st.session_state.source, 
                st.session_state.destination, 
                "Journey Completed"
            )
            st.toast(t["completed"], icon="🎉")
            st.balloons()
            if st.button("Plan Another Journey"):
                for key in ['tracking', 'reached', 'original_eta_mins', 'current_live_eta', 'previous_eta', 'source', 'destination', 'monsoon_active', 'selected_line', 'journey_id']:
                    if key in st.session_state: del st.session_state[key]
                st.rerun()
                
        if st.session_state.tracking:
            st.markdown(t["map_title"])
            start_coords = get_coordinates(st.session_state.source)
            end_coords = get_coordinates(st.session_state.destination)
            m = folium.Map(location=[(start_coords[0]+end_coords[0])/2, (start_coords[1]+end_coords[1])/2], zoom_start=11)
            folium.Marker(start_coords, popup=st.session_state.source, icon=folium.Icon(color='green', icon='play')).add_to(m)
            folium.Marker(end_coords, popup=st.session_state.destination, icon=folium.Icon(color='red', icon='stop')).add_to(m)
            folium.PolyLine([start_coords, end_coords], color="blue", weight=3).add_to(m)
            st_folium(m, width=800, height=350)
            
            st.markdown(t["dashboard"])
            dash_placeholder = st.empty()
            
            st.session_state.current_live_eta = get_fluctuated_eta(st.session_state.current_live_eta)
            current_time = datetime.now().strftime("%I:%M:%S %p")
            
            density_percent, crowd_status = predict_crowd_density(st.session_state.source, st.session_state.destination, st.session_state.monsoon_active)
            crowd_display = f"{density_percent}% ({crowd_status})"
            next_train_eta = f"{random.randint(2, 6)} mins"
            
            if st.session_state.current_live_eta != st.session_state.previous_eta:
                delta_diff = st.session_state.current_live_eta - st.session_state.previous_eta
                log_journey_sql(
                    st.session_state.journey_id, 
                    st.session_state.username, 
                    st.session_state.selected_line, 
                    st.session_state.source, 
                    st.session_state.destination, 
                    f"ETA Updated: {st.session_state.current_live_eta}m"
                )
                
                if delta_diff > 0: 
                    st.toast(f" Alert: ⚠️ Delay! ETA increased by {delta_diff} mins.", icon="📲")
                elif delta_diff < 0: 
                    st.toast(f" Alert: ⚡ Fast Route! Arriving {abs(delta_diff)} mins early.", icon="📲")
                st.session_state.previous_eta = st.session_state.current_live_eta

            with dash_placeholder.container():
                c1, c2, c3 = st.columns(3)
                c1.metric(t["orig_eta"], f"{st.session_state.original_eta_mins} mins")
                c2.metric(t["live_eta"], f"{st.session_state.current_live_eta} mins", delta=st.session_state.current_live_eta - st.session_state.original_eta_mins, delta_color="inverse")
                c3.metric(t["sync"], current_time)
                
                st.markdown(t["insights"])
                c4, c5, c6 = st.columns(3)
                c4.metric(t["crowd"], crowd_display)
                c5.metric(t["next_train"], next_train_eta)
                c6.metric(t["weather"], "Yes" if st.session_state.monsoon_active else "No")

            st.markdown("---")
            st.markdown("### 🛡️ Safety & Hazard Alerts")
            
            hazard_warning = get_station_hazard(st.session_state.destination)
            if "⚠️" in hazard_warning:
                st.warning(f"**Destination Hazard ({st.session_state.destination}):** {hazard_warning}")
            else:
                st.success(f"**Destination ({st.session_state.destination}):** {hazard_warning}")

            deboarding_alert = check_deboarding_risk(st.session_state.current_live_eta)
            if deboarding_alert:
                st.error(deboarding_alert, icon="🛑")

            with st.expander("🚨 Guardian Mode (Women's Safety)"):
                st.info(get_womens_helpline())
                if st.button("🔴 TRIGGER SOS ALERT", use_container_width=True):
                    emergency_data = trigger_sos_alert(st.session_state.username, st.session_state.source)
                    log_journey_sql(
                        st.session_state.journey_id, 
                        st.session_state.username, 
                        st.session_state.selected_line, 
                        st.session_state.source, 
                        st.session_state.destination, 
                        "🚨 SOS EMERGENCY"
                    )
                    
                    st.error(f"SOS Triggered! Authorities notified.")
                    st.code(f"Share this Live Tracking Link with family:\n{emergency_data['share_link']}")

            st.caption("🔄 Auto-refreshing every 10 seconds for demo...")
            time.sleep(10)
            st.rerun()

if __name__ == "__main__":
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()