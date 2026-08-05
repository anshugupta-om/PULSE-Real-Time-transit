import time
import random
import hashlib
import folium
from datetime import datetime
import streamlit as st
from streamlit_folium import st_folium

# Import Modular Engines
from copilot_engine import render_safety_copilot
from calendar_widget import render_technical_sidebar_calendar
from disruption_engine import render_disruption_and_rerouter, render_admin_disruption_control
from offline_safety import render_offline_womens_safety, render_admin_offline_logs, append_to_master_csv

# Import Modular Components
from config import LANGUAGES, MUMBAI_LOCATIONS, KNOWN_COORDS
from auth_manager import init_auth_db, login_page
from ai_predictor import predict_crowd_density
from digital_twin_ui import render_digital_twin
from panic_detector import render_safety_system
from chatbot_engine import pulse_chatbot
from weather_fx import render_weather_background

try:
    from db_manager import log_journey_sql, get_admin_dataframe, clear_all_data, get_next_journey_id
    from womens_safety import get_womens_helpline, trigger_sos_alert
    from accident_prevention import get_station_hazard, check_deboarding_risk
    MODULES_LOADED = True
except ImportError as e:
    st.error(f"⚠️ Missing Module: {e}")
    MODULES_LOADED = False

st.set_page_config(page_title="PULSE - Live Mumbai Navigator", layout="wide")
init_auth_db()

# Session State Setup
for key, default in [('logged_in', False), ('username', ""), ('role', None), ('tracking', False), ('journey_id', None), ('current_live_eta', 0), ('previous_eta', 0)]:
    if key not in st.session_state:
        st.session_state[key] = default

def get_coordinates(loc_name):
    if loc_name in KNOWN_COORDS: return KNOWN_COORDS[loc_name]
    h = int(hashlib.md5(loc_name.encode()).hexdigest(), 16)
    return [19.0760 + (h%100 - 50)/1000.0, 72.8777 + (h%100 - 50)/1000.0]

def main_app():
    if not MODULES_LOADED: return

    st.sidebar.header("⚙️ Settings")
    selected_lang = st.sidebar.selectbox("Language / भाषा:", ["English", "Hindi", "Marathi"])
    t = LANGUAGES[selected_lang]
    st.sidebar.markdown("---")

    if st.sidebar.button("Logout 🚪", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    # 📅 Live Technical Telemetry Calendar & Clock HUD Call
    render_technical_sidebar_calendar()

    badge = " Admin" if st.session_state.role == "admin" else " Commuter"
    st.title(f" Welcome, {st.session_state.username}! ({badge})")
    
    # 👑 IF ADMIN LOGGED IN: Render Controls & CSV Master Logs
    if st.session_state.role == "admin":
        render_admin_disruption_control()
        st.markdown("---")
        render_admin_offline_logs()
        st.markdown("---")

    st.markdown(f"### {t['title']}")

    # Phase 1: Planning Journey
    if not st.session_state.tracking:
        selected_line = st.selectbox(t["line"], ["Western Line", "Central Line", "Harbour Line"])
        col1, col2 = st.columns(2)
        with col1: source = st.selectbox(t["from"], MUMBAI_LOCATIONS, index=0)
        with col2: destination = st.selectbox(t["to"], MUMBAI_LOCATIONS, index=4)
        is_monsoon = st.checkbox(t["monsoon"])

        if st.button(t["start"]):
            if source == destination:
                st.warning(t["same_loc"])
            else:
                initial_eta = random.randint(25, 45) + (20 if is_monsoon else 0)
                st.session_state.journey_id = get_next_journey_id()
                log_journey_sql(st.session_state.journey_id, st.session_state.username, selected_line, source, destination, f"Started (ETA: {initial_eta}m)")
                st.session_state.update({
                    'tracking': True, 
                    'original_eta_mins': initial_eta, 
                    'current_live_eta': initial_eta, 
                    'previous_eta': initial_eta, 
                    'source': source, 
                    'destination': destination, 
                    'monsoon_active': is_monsoon, 
                    'selected_line': selected_line
                })
                st.rerun()

        # Render Commuter Disruption Alert (PERSISTENT FILE BROADCAST)
        render_disruption_and_rerouter()
        
        pulse_chatbot()

    # Phase 2: Live Tracking
    else:
        st.success(f"{t['tracking_msg']} **{st.session_state.source}** ➡️ **{st.session_state.destination}** via **{st.session_state.selected_line}**")
        if st.checkbox("✅ I have reached my destination!"):
            st.session_state.tracking = False
            log_journey_sql(st.session_state.journey_id, st.session_state.username, st.session_state.selected_line, st.session_state.source, st.session_state.destination, "Journey Completed")
            st.toast(t["completed"], icon="🎉")
            st.balloons()
            st.rerun()

        if st.session_state.tracking:
            render_disruption_and_rerouter()

            density_percent, crowd_status, live_weather = predict_crowd_density(
                st.session_state.source, 
                st.session_state.destination, 
                st.session_state.monsoon_active
            )

            render_weather_background(live_weather['status'], st.session_state.monsoon_active, st.session_state.source)

            st.markdown("### 🗺️ Dynamic Live Route & Spatial Tracker")
            map_col, info_col = st.columns([2, 1])
            
            with map_col:
                start_coords, end_coords = get_coordinates(st.session_state.source), get_coordinates(st.session_state.destination)
                m = folium.Map(
                    location=[(start_coords[0]+end_coords[0])/2, (start_coords[1]+end_coords[1])/2], 
                    zoom_start=11, 
                    tiles="CartoDB dark_matter"
                )
                folium.Marker(start_coords, popup=f"Source: {st.session_state.source}", icon=folium.Icon(color='green', icon='play')).add_to(m)
                folium.Marker(end_coords, popup=f"Destination: {st.session_state.destination}", icon=folium.Icon(color='red', icon='stop')).add_to(m)
                folium.PolyLine([start_coords, end_coords], color="#4da6ff", weight=4, opacity=0.85).add_to(m)
                st_folium(m, use_container_width=True, height=360)

            with info_col:
                st.markdown(
                    f"""
                    <div style="background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.1); height: 360px; display: flex; flex-direction: column; justify-content: space-around;">
                        <h4 style="margin:0; color:#4da6ff; font-size:18px;">📍 Active Route Overview</h4>
                        <p style="margin:5px 0; color:#ddd; font-size:14px;"><b>Source:</b> {st.session_state.source}</p>
                        <p style="margin:5px 0; color:#ddd; font-size:14px;"><b>Destination:</b> {st.session_state.destination}</p>
                        <p style="margin:5px 0; color:#ddd; font-size:14px;"><b>Transit Line:</b> {st.session_state.selected_line}</p>
                        <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;">
                        <div style="background: rgba(0,230,118,0.1); border-left: 4px solid #00e676; padding: 10px; border-radius: 6px;">
                            <span style="color: #00e676; font-size:12px; font-weight:bold;">🟢 GPS TELEMETRY ACTIVE</span><br>
                            <span style="color: #bbb; font-size:12px;">Satellite signals locked. Inter-station distance synced.</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            c1, c2, c3 = st.columns(3)
            c1.metric(t["orig_eta"], f"{st.session_state.original_eta_mins} mins")
            c2.metric(t["live_eta"], f"{st.session_state.current_live_eta} mins")
            c3.metric(t["sync"], datetime.now().strftime("%I:%M:%S %p"))

            c4, c5, c6 = st.columns(3)
            c4.metric(t["crowd"], f"{density_percent}% ({crowd_status})")
            c5.metric(t["next_train"], "3 mins")
            c6.metric("🌧️ Live Mumbai Weather", f"{live_weather['temp']} ({live_weather['status']})")

            avg_coach_crowd = render_digital_twin(density_percent)
            render_safety_system(st.session_state.source, avg_coach_crowd)
            render_safety_copilot(st.session_state.source, st.session_state.destination, density_percent, live_weather['status'])

            st.markdown("---")
            st.markdown("### 🛡️ Safety & Hazard Alerts")
            hazard_warning = get_station_hazard(st.session_state.destination)
            
            if "⚠️" in hazard_warning:
                st.warning(f"**Destination Hazard ({st.session_state.destination}):** {hazard_warning}")
            else:
                st.write(f"**Destination ({st.session_state.destination}):** {hazard_warning}")

            with st.expander("🚨 Guardian Mode (Online Women's Safety)"):
                st.info(get_womens_helpline())
                if st.button("🔴 TRIGGER ONLINE SOS ALERT", use_container_width=True):
                    emergency_data = trigger_sos_alert(st.session_state.username, st.session_state.source)
                    
                    # Appends Online Trigger to CSV Master File
                    append_to_master_csv(
                        st.session_state.username, 
                        "Logged-In Account", 
                        st.session_state.source, 
                        "Live Train Route", 
                        "ONLINE_SOS_TRIGGERED", 
                        "ONLINE_4G_5G"
                    )
                    
                    st.error("SOS Triggered! Authorities notified.")
                    st.code(f"Share Live Link:\n{emergency_data['share_link']}")

            st.caption("🔄 Auto-refreshing every 30 seconds...")
            time.sleep(30)
            st.rerun()

if __name__ == "__main__":
    if not st.session_state.logged_in:
        # 1. Render Normal Authentication Page
        login_page()
        
        # 2. 🚨 DIRECT UNAUTHENTICATED OFFLINE ACCESS (No Login Needed!)
        st.markdown("---")
        st.markdown("### 🚨 Direct Offline Emergency Access (Zero Login Required)")
        st.caption("In case of immediate underground panic or zero network, trigger offline SOS directly without logging in.")
        render_offline_womens_safety()
    else: 
        main_app()