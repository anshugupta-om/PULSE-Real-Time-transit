# chatbot_engine.py - Clean Floating Mascot ("Pulse Buddy") - Clipping Bug Fixed

import streamlit as st
import time
import random
from datetime import datetime
import streamlit.components.v1 as components

# Safe Import
try:
    from db_manager import log_chat_message
except ImportError:
    def log_chat_message(user, action_type, details, mode):
        print(f"[CHAT LOG] User: {user} | Action: {action_type} | Details: {details} | Mode: {mode}")

def get_robot_avatar_html(status_color="#00e5ff", eyes_svg=""):
    if not eyes_svg:
        eyes_svg = """
        <svg width="60" height="35" viewBox="0 0 70 40" class="blinking-eyes">
            <path d="M 12,25 Q 22,10 32,25" stroke="#00e5ff" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M 38,25 Q 48,10 58,25" stroke="#00e5ff" stroke-width="5" fill="none" stroke-linecap="round"/>
        </svg>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 12px 0 0 0; /* Top padding added so bounce does not clip antenna */
                background: transparent;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }}
            @keyframes eyeBlink {{
                0%, 90%, 100% {{ opacity: 1; transform: scaleY(1); }}
                95% {{ opacity: 0.2; transform: scaleY(0.1); }}
            }}
            .blinking-eyes {{
                animation: eyeBlink 3.5s infinite;
                transform-origin: center;
            }}
            @keyframes floatCuteRobo {{
                0%, 100% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-7px); }}
            }}
            @keyframes armWaveGesture {{
                0%, 100% {{ transform: rotate(0deg); }}
                50% {{ transform: rotate(-32deg); }}
            }}
            .robot-wrapper {{
                animation: floatCuteRobo 3.2s ease-in-out infinite;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            .robot-head {{
                width: 95px;
                height: 75px;
                background: linear-gradient(145deg, #f1f5f9, #94a3b8);
                border-radius: 28px 28px 20px 20px;
                position: relative;
                box-shadow: 0 10px 20px rgba(0,0,0,0.45);
                border: 2px solid #cbd5e1;
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 2;
            }}
            .robot-visor {{
                width: 75px;
                height: 52px;
                background: #020617;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 2px solid {status_color};
                box-shadow: 0 0 14px {status_color};
            }}
            .robot-torso {{
                width: 70px;
                height: 48px;
                background: linear-gradient(145deg, #cbd5e1, #64748b);
                border-radius: 14px 14px 22px 22px;
                margin-top: -6px;
                position: relative;
                box-shadow: 0 6px 14px rgba(0,0,0,0.3);
                border: 1.5px solid #94a3b8;
                z-index: 1;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .core-badge {{
                width: 16px;
                height: 16px;
                border-radius: 50%;
                background: #020617;
                border: 1.5px solid {status_color};
                box-shadow: 0 0 8px {status_color};
            }}
            .left-arm, .right-arm {{
                width: 14px;
                height: 36px;
                background: linear-gradient(145deg, #94a3b8, #475569);
                border-radius: 8px;
                position: absolute;
                top: 4px;
                border: 1px solid #cbd5e1;
            }}
            .left-arm {{ left: -11px; transform-origin: top right; animation: armWaveGesture 2s ease-in-out infinite; }}
            .right-arm {{ right: -11px; transform-origin: top left; }}
        </style>
    </head>
    <body>
        <div class="robot-wrapper">
            <div class="robot-head">
                <div class="robot-visor">
                    {eyes_svg}
                </div>
            </div>
            <div class="robot-torso">
                <div class="left-arm"></div>
                <div class="core-badge"></div>
                <div class="right-arm"></div>
            </div>
        </div>
    </body>
    </html>
    """

def inject_clean_corner_css():
    st.markdown("""
    <style>
    /* Gradient Colorful Text Styling */
    @keyframes textGlowPulse {
        0% { text-shadow: 0 0 10px rgba(0,229,255,0.6); }
        50% { text-shadow: 0 0 20px rgba(236,72,153,0.8); }
        100% { text-shadow: 0 0 10px rgba(0,229,255,0.6); }
    }

    .colorful-bot-label {
        background: linear-gradient(90deg, #00e5ff 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 15px;
        text-align: center;
        letter-spacing: 0.5px;
        animation: textGlowPulse 2.5s infinite alternate;
        margin-top: 2px;
        white-space: nowrap;
    }

    .stButton > button[key="open_buddy_chat_btn"] {
        border-radius: 20px !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, rgba(0,229,255,0.2) 0%, rgba(168,85,247,0.3) 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 229, 255, 0.6) !important;
        box-shadow: 0 0 15px rgba(0,229,255,0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button[key="open_buddy_chat_btn"]:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 25px rgba(168,85,247,0.7) !important;
    }

    /* Expanded Chat Modal Box */
    .expanded-chat-window {
        background: rgba(15, 23, 42, 0.94) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(0, 229, 255, 0.35) !important;
        border-radius: 22px !important;
        padding: 20px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9) !important;
        margin-top: 15px;
    }

    .stChatMessage {
        background: rgba(30, 41, 59, 0.75) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def generate_mumbai_transit_reply(user_msg: str, user_name: str) -> tuple[str, str, str, str]:
    msg = user_msg.lower()

    if any(w in msg for w in ["hi", "hello", "hey", "hii", "kaise ho", "namaste"]):
        eyes = """
        <svg width="60" height="35" viewBox="0 0 70 40" class="blinking-eyes">
            <path d="M 12,25 Q 22,10 32,25" stroke="#00e676" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M 38,25 Q 48,10 58,25" stroke="#00e676" stroke-width="5" fill="none" stroke-linecap="round"/>
        </svg>
        """
        return (
            f"Arey Hey {user_name}! 👋 Main Pulse Buddy hoon! Aaj Local schedule, Metro QR tickets, ya Safety Help mein kya madad karoon?",
            "#00e676", eyes, "😃 Happy & Welcoming"
        )
    elif "english" in msg:
        eyes = """
        <svg width="60" height="35" viewBox="0 0 70 40" class="blinking-eyes">
            <circle cx="22" cy="20" r="7" fill="#00e5ff"/>
            <circle cx="48" cy="20" r="7" fill="#00e5ff"/>
        </svg>
        """
        return (
            f"Sure {user_name}! I am fluent in English. Ask me about Suburban/Metro ticketing, interchange routes, or emergency safety alerts!",
            "#00e5ff", eyes, "🌐 English Mode"
        )
    elif any(w in msg for w in ["ticket", "qr", "pass", "uts", "fare"]):
        eyes = """
        <svg width="60" height="35" viewBox="0 0 70 40" class="blinking-eyes">
            <circle cx="22" cy="20" r="7" fill="#ffb74d"/>
            <circle cx="48" cy="20" r="7" fill="#ffb74d"/>
        </svg>
        """
        return (
            f"🎟️ **Mumbai Ticketing Guide:**\n\n"
            f"* **Suburban Local Trains:** Book UTS Paperless Tickets / Season Passes via UTS App.\n"
            f"* **Metro Lines:** Digital QR Tickets via WhatsApp or Metro Official App.\n"
            f"💡 *Tip:* Peak hours mein UTS Season Pass active rakhein queue skip karne ke liye!",
            "#ffb74d", eyes, "💳 Ticketing Assistance"
        )
    elif any(w in msg for w in ["interchange", "route", "dadar", "andheri", "ghatkopar"]):
        eyes = """
        <svg width="60" height="35" viewBox="0 0 70 40" class="blinking-eyes">
            <circle cx="22" cy="20" r="7" fill="#ffb74d"/>
            <circle cx="48" cy="20" r="7" fill="#ffb74d"/>
        </svg>
        """
        return (
            f"🔁 **Key Mumbai Interchange Hubs:**\n\n"
            f"* **Ghatkopar:** Central Local Line ↔ Metro Line 1\n"
            f"* **Andheri:** Western Local Line ↔ Metro Line 1\n"
            f"* **Dadar Hub:** Western ↔ Central Local Line Transfer",
            "#ffb74d", eyes, "🗺️ Route Hub Mode"
        )
    elif any(w in msg for w in ["helpline", "number", "police", "rpf"]):
        log_chat_message(user_name, "HELPLINE_QUERY", user_msg, "System")
        eyes = """
        <svg width="60" height="35" viewBox="0 0 70 40" class="blinking-eyes">
            <circle cx="22" cy="20" r="8" fill="#ff1744"/>
            <circle cx="48" cy="20" r="8" fill="#ff1744"/>
        </svg>
        """
        return (
            f"📞 **Official Helpline Numbers:**\n\n"
            f"* 🛡️ **Railway Police (RPF/GRP):** `1512` / `182`\n"
            f"* 👩 **Women Safety Helpline:** `103` / `1091`\n"
            f"* 🚆 **Mumbai Metro Helpline:** `1800 221 088`",
            "#ff1744", eyes, "🚨 Helpline Alert"
        )
    elif any(w in msg for w in ["harassment", "report", "unsafe"]):
        log_chat_message(user_name, "HARASSMENT_ALERT", user_msg, "Silent_Mode")
        eyes = """
        <svg width="60" height="35" viewBox="0 0 70 40" class="blinking-eyes">
            <path d="M 12,12 L 28,28 M 28,12 L 12,28" stroke="#ff1744" stroke-width="5" stroke-linecap="round"/>
            <path d="M 42,12 L 58,28 M 58,12 L 42,28" stroke="#ff1744" stroke-width="5" stroke-linecap="round"/>
        </svg>
        """
        return (
            f"🛡️ **Silent RPF Alert Triggered {user_name}!**\n\n"
            f"Aapka profile alert aur current station metadata RPF desk ko dispatch kar diya gaya hai. Agle stop par security monitor hoga.",
            "#ff1744", eyes, "🛡️ Silent RPF Active"
        )
    else:
        eyes = """
        <svg width="60" height="35" viewBox="0 0 70 40" class="blinking-eyes">
            <circle cx="22" cy="20" r="7" fill="#00e5ff"/>
            <circle cx="48" cy="20" r="7" fill="#00e5ff"/>
        </svg>
        """
        return (
            f"🤖 **PULSE AI Sync:** Main aapki query *'{user_msg}'* ko process kar raha hoon. UTS Tickets, Interchanges, ya Helplines ke baare mein poochiye!",
            "#00e5ff", eyes, "⚡ Transit Telemetry Sync"
        )

def pulse_chatbot():
    inject_clean_corner_css()
    
    current_user = st.session_state.get("username", "Commuter")
    
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False
    if "bot_color" not in st.session_state:
        st.session_state.bot_color = "#00e5ff"
    if "bot_eyes_svg" not in st.session_state:
        st.session_state.bot_eyes_svg = ""
    if "bot_status_title" not in st.session_state:
        st.session_state.bot_status_title = "🟢 Personal AI Copilot Active"

    # ----------------------------------------------------
    # STATE 1: ULTRA-CLEAN RIGHT-CORNER FLOATING MASCOT
    # ----------------------------------------------------
    if not st.session_state.chat_open:
        col_empty, col_right_corner = st.columns([3.8, 1.2])
        with col_right_corner:
            # 1. Floating Animated Robot (Height increased to 160 to prevent antenna clipping)
            robo_html = get_robot_avatar_html(st.session_state.bot_color, st.session_state.bot_eyes_svg)
            components.html(robo_html, height=160)
            
            # 2. Gradient Colorful Text Directly Below Robot
            st.markdown(
                '<div class="colorful-bot-label">✨ Hi, I am Pulse Buddy!<br><small style="font-size:11px; opacity:0.8;">Your Personal Assistant</small></div>', 
                unsafe_allow_html=True
            )
            
            st.write("") # Small Spacing
            
            # 3. Clean Tap Button
            if st.button("💬 Tap to Chat", key="open_buddy_chat_btn", use_container_width=True):
                st.session_state.chat_open = True
                st.rerun()

    # ----------------------------------------------------
    # STATE 2: EXPANDED INTERACTIVE CHAT PANEL
    # ----------------------------------------------------
    else:
        r_col1, r_col2 = st.columns([0.8, 4.2])
        with r_col1:
            robo_html = get_robot_avatar_html(st.session_state.bot_color, st.session_state.bot_eyes_svg)
            components.html(robo_html, height=150)
        with r_col2:
            st.markdown(f"""
            <div style="padding-top:10px;">
                <h3 style="color:#00e5ff; margin:0; font-weight:800;">Pulse Buddy (Personal AI Copilot)</h3>
                <span style="color:{st.session_state.bot_color}; font-weight:700; font-size:13px;">● {st.session_state.bot_status_title}</span>
            </div>
            """, unsafe_allow_html=True)

        col_close_btn, col_empty = st.columns([1.2, 3.8])
        with col_close_btn:
            if st.button("✖ Close Chat", key="close_chat_btn", use_container_width=True):
                st.session_state.chat_open = False
                st.rerun()

        # Messages History
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = [
                {
                    "role": "assistant", 
                    "content": f"Arey Hey {current_user}! 👋 Main aapka **Pulse Buddy** hoon. Metro/Local timings, UTS tickets, ya safety help ke liye poochiye!"
                }
            ]

        # Quick Actions
        st.caption("⚡ Quick Actions:")
        col_q1, col_q2, col_q3, col_q4 = st.columns(4)
        quick_action = None
        with col_q1:
            if st.button("🎫 QR & UTS Tickets", use_container_width=True):
                quick_action = "How to buy QR and UTS tickets?"
        with col_q2:
            if st.button("📞 Helplines", use_container_width=True):
                quick_action = "Show emergency helpline numbers"
        with col_q3:
            if st.button("🔀 Interchanges", use_container_width=True):
                quick_action = "Show Metro and Local interchange stations"
        with col_q4:
            if st.button("📢 Harassment", use_container_width=True):
                quick_action = "Report Seat Harassment (Discreet)"

        chat_container = st.container(height=300)
        with chat_container:
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        user_input = st.chat_input("Talk to Pulse Buddy (e.g., 'Hello', 'Helpline numbers')...")

        if quick_action:
            user_input = quick_action

        if user_input:
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            
            bot_reply, color_code, eyes_code, status_title = generate_mumbai_transit_reply(user_input, current_user)
            st.session_state.bot_color = color_code
            st.session_state.bot_eyes_svg = eyes_code
            st.session_state.bot_status_title = status_title

            st.session_state.chat_messages.append({"role": "assistant", "content": bot_reply})
            st.rerun()