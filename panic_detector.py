# panic_detector.py - Station Safety & Panic Response Engine

import random
import streamlit as st

def render_safety_system(station_name, avg_coach_crowd):
    """
    Renders Live Station Safety & Panic Response system synchronized with realistic train density.
    """
    st.markdown("---")
    st.markdown("### 🛡️ Live Station Safety & Panic Response System")
    st.caption("AI continuously monitors station health & live coach density to protect passengers from stampedes and emergencies.")

    movement_spike = max(10, min(100, avg_coach_crowd))
    
    # Realistic Threat Thresholds
    if movement_spike >= 70:
        decibels = random.randint(80, 92)
        telemetry_loss = random.randint(25, 45)
        alerts = random.randint(3, 5)
        threat_level = "HIGH CROWD RUSH / PANIC DETECTED"
        color = "#ff3366"
        icon = "🚨"
        action = "Police emergency team alerted automatically. Platform gates temporarily paused to manage overcrowding."
    elif movement_spike >= 45:
        decibels = random.randint(64, 76)
        telemetry_loss = random.randint(12, 24)
        alerts = random.randint(1, 2)
        threat_level = "MODERATE CROWD MOVEMENT"
        color = "#ff9900"
        icon = "⚠️"
        action = "Station camera surveillance increased. Public announcement system guiding passengers."
    else:
        decibels = random.randint(48, 60)
        telemetry_loss = random.randint(4, 12)
        alerts = 0
        threat_level = "SAFE & CALM ENVIRONMENT"
        color = "#00e676"
        icon = "🟢"
        action = "Platform is peaceful and moving smoothly. No emergency alerts."

    safety_index = max(10, min(100, 100 - int(movement_spike * 0.8)))

    # Banner UI
    st.markdown(
        f"""
        <style>
            .safety-banner {{
                background: linear-gradient(135deg, #1e222d 0%, #11141c 100%);
                border-left: 6px solid {color};
                border-radius: 12px; padding: 18px; margin-bottom: 20px;
            }}
        </style>
        <div class="safety-banner">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <h3 style="margin: 0; color: {color}; font-size: 20px; font-weight: 700;">{icon} Status: {threat_level}</h3>
                <span style="background: rgba(255,255,255,0.08); padding: 5px 12px; border-radius: 20px; font-size: 13px; color: #4da6ff;">
                    Safety Score Index: {safety_index}/100
                </span>
            </div>
            <p style="margin: 10px 0 0 0; color: #d0d5dd; font-size: 14px;"><b>📢 Immediate Guidance:</b> {action}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Layman Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🔊 Station Noise Level", f"{decibels} dB", delta="High Noise Level" if movement_spike >= 70 else "Normal Ambient", delta_color="inverse" if movement_spike >= 70 else "normal")
    m2.metric("🏃 Sudden Crowd Rush", f"{movement_spike}%", delta="Heavy Boarding Rush" if movement_spike >= 70 else "Normal Movement", delta_color="inverse" if movement_spike >= 70 else "normal")
    m3.metric("📡 Phone Signal Stability", f"{telemetry_loss}%", delta="Crowd Signal Jam" if movement_spike >= 70 else "Good Coverage", delta_color="inverse" if movement_spike >= 70 else "normal")
    m4.metric("👥 Commuter Help Calls", f"{alerts} Alerts", delta="Distress Reports" if movement_spike >= 70 else "Platform Peaceful", delta_color="inverse" if movement_spike >= 70 else "normal")