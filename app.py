import streamlit as st
from datetime import datetime
import time
import random
import folium
from streamlit_folium import st_folium
import hashlib
import os

# --- CUSTOM MODULES IMPORTS ---
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
    st.session_state.journey_id = None # Track Serial Number
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
# 🔐 FEATURE 1: DUAL LOGIN PAGE (USER & ADMIN)
# ==========================================
def login_page():
    st.markdown("<h1 style='text-align: center;'>🚆 Welcome to PULSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Live Mumbai Transit Navigator</p><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🚇 Commuter (Public)", "🛠️ Admin Portal"])
        with tab1:
            st.markdown("Join thousands of Mumbaikars tracking their daily transit.")
            user_name = st.text_input("Enter your Name:")
            if st.button("Start My Journey 🚀"):
                if user_name.strip() != "":
                    st.session_state.logged_in = True
                    st.session_state.username = user_name.title()
                    st.session_state.role = "user"
                    st.success(f"Welcome {user_name}! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Please enter your name to continue.")
        with tab2:
            st.markdown("For Transit Authorities & Admins only.")
            admin_user = st.text_input("Admin Username")
            admin_pass = st.text_input("Password", type="password")
            if st.button("Login as Admin 🔐"):
                if admin_user.lower() == "anshu" and admin_pass == "1234":
                    st.session_state.logged_in = True
                    st.session_state.username = "Admin Anshu"
                    st.session_state.role = "admin"
                    st.success("Admin Login Successful! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid Credentials. (Hint: anshu / 1234)")

# ==========================================
# 🚀 MAIN APP
# ==========================================
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

    # --- SIDEBAR: SETTINGS & ADMIN SQL PANEL ---
    st.sidebar.header("⚙️ Settings")
    selected_lang = st.sidebar.selectbox("Language / भाषा:", ["English", "Hindi", "Marathi"])
    t = LANGUAGES[selected_lang]
    st.sidebar.markdown("---")
    
    if st.session_state.role == "admin":
        st.sidebar.header("🛠️ Admin Panel (SQL)")
        try:
            admin_df = get_admin_dataframe()
            if not admin_df.empty:
                # --- 🚨 ACTIVE SOS MONITORING FOR ADMIN 🚨 ---
                sos_alerts = admin_df[admin_df['Status'] == "🚨 SOS EMERGENCY"]
                if not sos_alerts.empty:
                    st.sidebar.markdown("---")
                    st.sidebar.error("🚨 **ACTIVE SOS EMERGENCIES** 🚨")
                    for index, row in sos_alerts.head(3).iterrows():
                        st.sidebar.warning(f"👤 **User:** {row['User']}\n\n📍 **Location:** {row['From']} to {row['To']}\n\n🕒 **Time:** {row['Time']}")
                    st.sidebar.markdown("---")
                
                # Show Full Dataframe
                st.sidebar.dataframe(admin_df, use_container_width=True) 
                
                # Download Button
                csv_data = admin_df.to_csv(index=False).encode('utf-8')
                st.sidebar.download_button(
                    label="📥 Download SQL Data (CSV)",
                    data=csv_data,
                    file_name="pulse_sql_export.csv",
                    mime="text/csv"
                )
                
                # Clear Database Button
                st.sidebar.markdown("---")
                if st.sidebar.button("🗑️ Clear All Data (Reset DB)", type="primary"):
                    clear_all_data()
                    st.sidebar.success("Database Cleared! Refreshing...")
                    time.sleep(1)
                    st.rerun()
                    
                st.sidebar.success("SQL Database Active 🟢")
            else:
                st.sidebar.info("Database is empty.")
        except Exception as e:
            st.sidebar.error("Database initializing...")
        st.sidebar.markdown("---")

    if st.sidebar.button("Logout 🚪"):
        st.session_state.clear()
        st.rerun()

    # --- UI: TITLES ---
    badge = "🛠️ Admin" if st.session_state.role == "admin" else "👤 Commuter"
    st.title(f"👋 Welcome, {st.session_state.username}! ({badge})")
    st.markdown(f"### {t['title']}")

    # ==========================================
    # PHASE 1: ENTERING LOCATION & STARTING
    # ==========================================
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
                    
                    # --- 🎯 1. SQL LOGGING: START JOURNEY ---
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

    # ==========================================
    # PHASE 2: LIVE TRACKING, MAP & ALERTS
    # ==========================================
    else:
        st.success(f"{t['tracking_msg']} **{st.session_state.source}** ➡️ **{st.session_state.destination}** via **{st.session_state.selected_line}**")
        
        if st.checkbox("✅ I have reached my destination!"):
            st.session_state.tracking = False
            # --- 🎯 2. SQL LOGGING: JOURNEY COMPLETED ---
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
            # 🗺️ MAP DISPLAY
            st.markdown(t["map_title"])
            start_coords = get_coordinates(st.session_state.source)
            end_coords = get_coordinates(st.session_state.destination)
            m = folium.Map(location=[(start_coords[0]+end_coords[0])/2, (start_coords[1]+end_coords[1])/2], zoom_start=11)
            folium.Marker(start_coords, popup=st.session_state.source, icon=folium.Icon(color='green', icon='play')).add_to(m)
            folium.Marker(end_coords, popup=st.session_state.destination, icon=folium.Icon(color='red', icon='stop')).add_to(m)
            folium.PolyLine([start_coords, end_coords], color="blue", weight=3).add_to(m)
            st_folium(m, width=800, height=350)
            
            # 📡 DASHBOARD
            st.markdown(t["dashboard"])
            dash_placeholder = st.empty()
            
            st.session_state.current_live_eta = get_fluctuated_eta(st.session_state.current_live_eta)
            current_time = datetime.now().strftime("%I:%M:%S %p")
            
            # --- AI CROWD PREDICTOR ---
            density_percent, crowd_status = predict_crowd_density(st.session_state.source, st.session_state.destination, st.session_state.monsoon_active)
            crowd_display = f"{density_percent}% ({crowd_status})"
            next_train_eta = f"{random.randint(2, 6)} mins"
            
            # NOTIFICATION & SQL SAVE ON CHANGE
            if st.session_state.current_live_eta != st.session_state.previous_eta:
                delta_diff = st.session_state.current_live_eta - st.session_state.previous_eta
                # --- 🎯 3. SQL LOGGING: ETA UPDATED ---
                log_journey_sql(
                    st.session_state.journey_id, 
                    st.session_state.username, 
                    st.session_state.selected_line, 
                    st.session_state.source, 
                    st.session_state.destination, 
                    f"ETA Updated: {st.session_state.current_live_eta}m"
                )
                
                if delta_diff > 0: 
                    st.toast(f"📱 Alert: ⚠️ Delay! ETA increased by {delta_diff} mins.", icon="📲")
                elif delta_diff < 0: 
                    st.toast(f"📱 Alert: ⚡ Fast Route! Arriving {abs(delta_diff)} mins early.", icon="📲")
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

            # --- SAFETY & ACCIDENT PREVENTION UI ---
            st.markdown("---")
            st.markdown("### 🛡️ Safety & Hazard Alerts")
            
            # 1. Accident Prevention: Station Hazard Info
            hazard_warning = get_station_hazard(st.session_state.destination)
            if "⚠️" in hazard_warning:
                st.warning(f"**Destination Hazard ({st.session_state.destination}):** {hazard_warning}")
            else:
                st.success(f"**Destination ({st.session_state.destination}):** {hazard_warning}")

            # 2. Accident Prevention: Door Rushing Alert
            deboarding_alert = check_deboarding_risk(st.session_state.current_live_eta)
            if deboarding_alert:
                st.error(deboarding_alert, icon="🛑")

            # 3. Women's Safety: Guardian Mode
            with st.expander("🚨 Guardian Mode (Women's Safety)"):
                st.info(get_womens_helpline())
                if st.button("🔴 TRIGGER SOS ALERT", use_container_width=True):
                    # --- 🎯 4. SQL LOGGING: SOS ALERT ---
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