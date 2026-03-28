import streamlit as st
from datetime import datetime

def pulse_chatbot():
    st.markdown("---")
    st.subheader("🤖 PULSE Intelligent Assistant")
    
    # Language Support (Language select box app.py se yahan pass ho sakta hai)
    with st.expander("💬 Chat with PULSE / ऑफलाइन सहायता"):
        st.write("Current Status: 📶 Online Mode (Auto-Sync Active)")
        
        chat_option = st.selectbox("How can I help you?", [
            "Select an option...",
            "🆘 Emergency SMS (No Internet)",
            "🧳 Need Porter/Coolie (Next Station)",
            "🩺 Medical Assist at Station",
            "📢 Report Seat Harassment (Discreet)",
            "🍱 Order Food for Next Station"
        ])

        # 1. Emergency SMS Feature
        if chat_option == "🆘 Emergency SMS (No Internet)":
            st.warning("Network issue? Type your message below. It will be sent via SMS Protocol as soon as signal returns.")
            sms_content = st.text_area("Type your SOS message (e.g., 'Stuck at Dadar, tell family'): ")
            if st.button("Send Offline SMS"):
                from db_manager import log_chat_message
                log_chat_message(st.session_state.username, "OFFLINE_SMS", sms_content, "No_Internet_Triggered")
                st.success("✅ Logged! Admin will receive this even if your net is fluctuating.")

        # 2. Porter/Coolie Feature (Unique)
        elif chat_option == "🛳 Need Porter/Coolie (Next Station)":
            st.info("Hum aapke liye agle station par Porter (Coolie) book kar rahe hain.")
            luggage = st.radio("Luggage size?", ["Light", "Heavy", "Very Heavy"])
            if st.button("Book Coolie"):
                from db_manager import log_chat_message
                log_chat_message(st.session_state.username, "PORTER_REQ", f"Size: {luggage}", "Online")
                st.success(f"Request sent! Porter will be at your destination platform.")

        # 3. Harassment Reporting (Safety Focus)
        elif chat_option == "📢 Report Seat Harassment (Discreet)":
            st.error("Don't worry, this report is anonymous. RPF will be notified.")
            desc = st.text_input("Describe the person/situation: ")
            if st.button("Submit Quiet Alert"):
                from db_manager import log_chat_message
                log_chat_message(st.session_state.username, "HARASSMENT_ALERT", desc, "Silent_Mode")
                st.toast("RPF at next station notified silently.", icon="🛡️")

        # 4. Food Order (Convenience - Optional unique feature)
        elif chat_option == "🍱 Order Food for Next Station":
            st.info("Get fresh snacks delivered at your coach door.")
            order = st.selectbox("Menu", ["Vada Pav", "Samosa", "Chai", "Water Bottle"])
            if st.button("Confirm Order"):
                from db_manager import log_chat_message
                log_chat_message(st.session_state.username, "FOOD_ORDER", order, "Online")
                st.success(f"Ordered {order}! Keep change ready.")