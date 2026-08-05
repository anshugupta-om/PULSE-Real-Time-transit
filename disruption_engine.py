# disruption_engine.py - Persistent File-Based Admin Broadcast Engine

import streamlit as st
import json
import os

STATUS_FILE = "disruption_status.json"

def get_disruption_data():
    """Reads saved disruption state from JSON file."""
    if not os.path.exists(STATUS_FILE):
        return {
            "active": False,
            "corridor": "Aqua Line 3 (Underground)",
            "reason": "Underground signal snag & single-track bottleneck."
        }
    try:
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"active": False, "corridor": "", "reason": ""}

def save_disruption_data(active, corridor, reason):
    """Saves disruption state to JSON file persistently across sessions/logouts."""
    data = {
        "active": active,
        "corridor": corridor,
        "reason": reason
    }
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)

def render_admin_disruption_control():
    """Rendered inside Admin Panel with diverse Real-World Disruption Scenarios."""
    st.markdown("### 🛠️ Admin Control: Transit Disruption Operations")
    
    current_data = get_disruption_data()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        scenario = st.selectbox(
            "Select Real-World Incident Scenario:", 
            [
                "Custom Manual Entry",
                "🌧️ Heavy Monsoon Waterlogging (Track Flooding at Kurla/Sion)",
                "⚡ Overhead Wire (OHE) Power Breakdown",
                "🚇 Aqua Line 3 Underground Signal Snag",
                "🛤️ Line 2A Single-Line Bottleneck"
            ]
        )
        
        if scenario == "Custom Manual Entry":
            corridor = st.text_input("Affected Corridor:", "Western Local Line")
            reason = st.text_input("Snag Cause / Details:", "Emergency track maintenance in progress.")
        elif "Waterlogging" in scenario:
            corridor = "Central Line (Kurla - Sion Sector)"
            reason = "Tracks submerged under 4 inches of rain. Trains running 30 mins late."
        elif "Overhead" in scenario:
            corridor = "Western Line (Dadar - Bandra Sector)"
            reason = "OHE power cable failure. Train services paused at Dadar."
        elif "Aqua Line" in scenario:
            corridor = "Aqua Line 3 (T2 Airport Underground)"
            reason = "Underground signal snag. Commuters stranded at platform."
        else:
            corridor = "Line 2A (Metro)"
            reason = "Single-line track bottleneck due to technical glitch."
    
    with col2:
        st.write(" ")
        st.write(" ")
        if current_data.get("active", False):
            if st.button("🟢 STOP / RESOLVE DISRUPTION", use_container_width=True):
                save_disruption_data(False, corridor, reason)
                st.success("Disruption Resolved Globally!")
                st.rerun()
        else:
            if st.button("🚨 TRIGGER LIVE BROADCAST", use_container_width=True):
                save_disruption_data(True, corridor, reason)
                st.error("Global Broadcast Sent to All Commuters!")
                st.rerun()
                
def render_disruption_and_rerouter():
    """Rendered on Commuter Dashboard persistently read from file."""
    current_data = get_disruption_data()
    
    # If no active snag triggered by Admin, return silently
    if not current_data.get("active", False):
        return

    st.markdown(
        f"""
        <div style="background: rgba(255, 23, 68, 0.12); border: 1.5px solid #ff1744; border-radius: 14px; padding: 16px; margin: 15px 0; box-shadow: 0 0 15px rgba(255, 23, 68, 0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="color: #ff1744; margin: 0; font-weight: 900;">🚨 LIVE TRANSIT DISRUPTION ALERT (BROADCAST)</h4>
                <span style="background: #ff1744; color: white; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: bold;">CRITICAL DELAY</span>
            </div>
            <p style="color: #e2e8f0; margin: 8px 0 4px 0; font-size: 13.5px;">
                <b>Affected Corridor:</b> <span style="color: #00e5ff;">{current_data.get('corridor')}</span><br>
                <b>Admin Advisory:</b> {current_data.get('reason')}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### 🔄 AI Recommended Alternate Feeder Routes")
    r1, r2 = st.columns(2)

    with r1:
        st.markdown(
            """
            <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 12px;">
                <div style="color: #ffb74d; font-weight: bold; font-size: 12px;">❌ Regular Transit Route</div>
                <h4 style="color: #ff1744; margin: 4px 0;">Delay: ~35 Mins</h4>
                <p style="color: #94a3b8; font-size: 11px; margin: 0;">Heavy platform congestion & stranded trains.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with r2:
        st.markdown(
            """
            <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #00e5ff; border-radius: 12px; padding: 12px; box-shadow: 0 0 10px rgba(0,229,255,0.2);">
                <div style="color: #00e5ff; font-weight: bold; font-size: 12px;">⚡ AI Bypass Route</div>
                <h4 style="color: #00e676; margin: 4px 0;">ETA: 14 Mins (Saved 20m)</h4>
                <p style="color: #cbd5e1; font-size: 11px; margin: 0;">🚌 BEST Feeder Bus B-302 ➡️ Shared Auto Stand Link</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("---")