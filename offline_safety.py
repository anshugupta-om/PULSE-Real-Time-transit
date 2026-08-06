# offline_safety.py - Persistent Offline Safety Engine with Custom & Dropdown Inputs

import streamlit as st
import json
import os
import datetime
import pandas as pd
import urllib.parse
import streamlit.components.v1 as components

CSV_MASTER_LOG = "emergency_master_logs.csv"

def append_to_master_csv(name, phone, location, coach, status, mode="OFFLINE"):
    """Appends incident details into a structured CSV file for Admin analysis."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    
    new_data = {
        "Timestamp": [timestamp],
        "Passenger_Name": [name if name else "Anonymous Passenger"],
        "Contact_No": [phone if phone else "N/A"],
        "Location": [location if location else "Unspecified Location"],
        "Coach_Area": [coach if coach else "Unspecified Area"],
        "Status_Flag": [status],
        "Connectivity_Mode": [mode]
    }
    
    df_new = pd.DataFrame(new_data)
    
    if not os.path.exists(CSV_MASTER_LOG):
        df_new.to_csv(CSV_MASTER_LOG, index=False)
    else:
        df_new.to_csv(CSV_MASTER_LOG, mode='a', header=False, index=False)

def render_admin_offline_logs():
    """Renders Master CSV Log Table & Download Options inside Admin Panel."""
    st.markdown("### 📊 Master Safety & Emergency Audit Logs (CSV Unified)")
    st.caption("Central CSV database containing both Online Commuter Journeys and Offline Zero-Net Distress Triggers.")
    
    if not os.path.exists(CSV_MASTER_LOG):
        st.info("🟢 No emergency distress incidents recorded in Master CSV.")
        return

    try:
        df_logs = pd.read_csv(CSV_MASTER_LOG)
        if df_logs.empty:
            st.info("🟢 Master CSV log is currently empty.")
            return

        st.dataframe(
            df_logs, 
            use_container_width=True,
            column_config={
                "Timestamp": "Incident Time",
                "Passenger_Name": "Passenger",
                "Contact_No": "Phone Number",
                "Location": "Location/Station",
                "Coach_Area": "Coach/Area",
                "Status_Flag": "Status",
                "Connectivity_Mode": "Network Mode"
            }
        )

        csv_data = df_logs.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Master Audit Logs (CSV)",
            data=csv_data,
            file_name=f"PULSE_Master_Emergency_Logs_{datetime.date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Error reading CSV Master Log: {e}")

def render_offline_womens_safety():
    st.markdown("### 🛡️ Guardian Mode: Zero-Net Offline Safety System")
    st.caption("Instant protection when cellular data/login is completely unavailable.")

    # 1. PASSENGER INPUT FORM WITH NEUTRAL PLACEHOLDERS
    st.markdown("##### 📝 Quick Offline Passenger Details (No Login Needed)")
    c_name, c_phone, c_loc, c_coach = st.columns(4)

    with c_name:
        p_name = st.text_input("Name:", placeholder="e.g. Passenger XYZ")
    with c_phone:
        p_phone = st.text_input("Emergency Phone:", placeholder="e.g. +91 XXXXX XXXXX")
    with c_loc:
        loc_choice = st.selectbox("Location / Station:", ["Aqua Line T2 Airport", "Churchgate Tunnel", "Dadar Platform 3", "Andheri Station", "Custom / Type Other..."])
        if loc_choice == "Custom / Type Other...":
            p_loc = st.text_input("Enter Custom Location:", placeholder="e.g. Malad FOB / Line 2A")
        else:
            p_loc = loc_choice
            
    with c_coach:
        coach_choice = st.selectbox("Coach / Area:", ["Coach C4 (Ladies)", "Coach C1", "Platform Dead Zone", "Staircase", "Custom / Type Other..."])
        if coach_choice == "Custom / Type Other...":
            p_coach = st.text_input("Enter Custom Area:", placeholder="e.g. Gate 2 / Mid-Aisle")
        else:
            p_coach = coach_choice

    st.markdown("---")

    col_sos, col_defense = st.columns([1, 1])

    with col_sos:
        st.markdown("#### 🚨 Emergency Offline Dispatch")
        
        loc_str = p_loc if p_loc else "Unknown Underground Spot"
        coach_str = p_coach if p_coach else "Unknown Area"
        name_str = p_name if p_name else "Passenger XYZ"
        phone_str = p_phone if p_phone else "+91 XXXXX XXXXX"
        
        raw_msg = f"EMERGENCY SOS! Stranded at {loc_str} ({coach_str}). Name: {name_str}, Contact: {phone_str}. Send RPF 139 immediately!"

        if st.button("🆘 TRIGGER OFFLINE PANIC SOS", type="primary", use_container_width=True):
            append_to_master_csv(p_name, p_phone, loc_str, coach_str, "OFFLINE_PANIC_TRIGGERED", "ZERO_NET_OFFLINE")
            
            st.error("🚨 Offline SOS Logged in Master CSV Queue for Admin!")
            st.info("📲 **Copy SOS Message Below (For Manual GSM SMS / WhatsApp):**")
            st.code(raw_msg, language="text")

    with col_defense:
        st.markdown("#### ⚡ Real JS Audio Siren & Visual Strobe")
        
        siren_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .btn-siren {
                    background: #ff1744; color: white; border: none; padding: 10px 15px;
                    border-radius: 6px; font-weight: bold; cursor: pointer; width: 48%; margin-right: 2%;
                }
                .btn-strobe {
                    background: #00e5ff; color: #020617; border: none; padding: 10px 15px;
                    border-radius: 6px; font-weight: bold; cursor: pointer; width: 48%;
                }
                #flash-overlay {
                    display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                    z-index: 99999;
                }
            </style>
            <script>
                let audioCtx = null;
                let osc = null;
                let isPlaying = false;
                let strobeInterval = null;

                function toggleSiren() {
                    if (!isPlaying) {
                        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                        osc = audioCtx.createOscillator();
                        let gain = audioCtx.createGain();
                        
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(800, audioCtx.currentTime);
                        
                        let now = audioCtx.currentTime;
                        osc.frequency.linearRampToValueAtTime(1200, now + 0.5);
                        osc.frequency.linearRampToValueAtTime(800, now + 1.0);
                        
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start();
                        isPlaying = true;
                        document.getElementById('sirenBtn').innerText = "🛑 STOP SIREN";
                    } else {
                        if (osc) osc.stop();
                        isPlaying = false;
                        document.getElementById('sirenBtn').innerText = "🔊 HIGH-DECIBEL SIREN";
                    }
                }

                function toggleStrobe() {
                    let overlay = document.getElementById('flash-overlay');
                    if (overlay.style.display === 'none' || overlay.style.display === '') {
                        overlay.style.display = 'block';
                        let state = false;
                        strobeInterval = setInterval(() => {
                            overlay.style.backgroundColor = state ? '#ffffff' : '#ff0000';
                            state = !state;
                        }, 80);
                    } else {
                        clearInterval(strobeInterval);
                        overlay.style.display = 'none';
                    }
                }
            </script>
        </head>
        <body style="background:transparent; margin:0; padding:0;">
            <div id="flash-overlay" onclick="toggleStrobe()"></div>
            <button id="sirenBtn" class="btn-siren" onclick="toggleSiren()">🔊 HIGH-DECIBEL SIREN</button>
            <button class="btn-strobe" onclick="toggleStrobe()">🔦 STROBE FLASH</button>
        </body>
        </html>
        """
        components.html(siren_html, height=55)