# disruption_engine.py - Broadcast Alert & Admin Rerouter Engine

import os
import streamlit as st

DISRUPTION_FILE = "disruption_broadcast.txt"

def get_active_disruption():
    if os.path.exists(DISRUPTION_FILE):
        with open(DISRUPTION_FILE, "r") as f:
            content = f.read().strip()
            if content:
                parts = content.split("||")
                if len(parts) == 3:
                    return {"corridor": parts[0], "level": parts[1], "msg": parts[2]}
    return None

def render_disruption_and_rerouter():
    alert = get_active_disruption()
    if alert:
        st.markdown(f"""
        <div style="background: rgba(225, 29, 72, 0.15); border: 1.5px solid #f43f5e; border-radius: 16px; padding: 18px 24px; margin-bottom: 20px; box-shadow: 0 0 20px rgba(244, 63, 94, 0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="color: #f43f5e; font-weight: 900; font-size: 16px; letter-spacing: 0.5px;">🚨 LIVE TRANSIT DISRUPTION ALERT (BROADCAST)</span>
                <span style="background: #f43f5e; color: #fff; font-size: 11px; font-weight: 800; padding: 3px 10px; border-radius: 12px; text-transform: uppercase;">{alert['level']}</span>
            </div>
            <p style="color: #fecdd3; font-size: 14px; margin: 0;"><b>Affected Corridor:</b> {alert['corridor']}<br><b>Admin Advisory:</b> {alert['msg']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🔄 AI Recommended Alternate Feeder Routes")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 16px;">
                <span style="color: #ef4444; font-weight: 800; font-size: 12px;">❌ Regular Transit Route</span>
                <h4 style="color: #f87171; margin: 6px 0;">Delay: ~35 Mins</h4>
                <small style="color: #94a3b8;">Heavy platform congestion & stranded trains.</small>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 14px; padding: 16px;">
                <span style="color: #10b981; font-weight: 800; font-size: 12px;">⚡ AI Bypass Route</span>
                <h4 style="color: #34d399; margin: 6px 0;">ETA: 14 Mins (Saved 20m)</h4>
                <small style="color: #a7f3d0;">🚌 BEST Feeder Bus B-302 ➔ Shared Auto Stand Link</small>
            </div>
            """, unsafe_allow_html=True)
        st.write("")

def render_admin_disruption_control():
    st.markdown("### 📡 Admin Disruption Control Desk")
    col1, col2 = st.columns([2, 1])
    with col1:
        corr = st.selectbox("Select Corridor:", ["Western Local Line", "Central Local Line", "Harbour Line", "Metro Line 1"])
        lvl = st.selectbox("Disruption Severity:", ["CRITICAL DELAY", "TRACK MAINTENANCE", "SUSPENDED SERVICE"])
        msg = st.text_input("Broadcast Advisory Message:", placeholder="e.g., Emergency track maintenance at Dadar.")
    with col2:
        st.write("")
        st.write("")
        if st.button("📢 Broadcast Alert", width="stretch"):
            if msg:
                with open(DISRUPTION_FILE, "w") as f:
                    f.write(f"{corr}||{lvl}||{msg}")
                st.success("Alert broadcasted live across network!")
                st.rerun()
        if st.button("🔴 Clear Active Alert", width="stretch"):
            if os.path.exists(DISRUPTION_FILE):
                os.remove(DISRUPTION_FILE)
            st.info("Broadcast alert cleared.")
            st.rerun()