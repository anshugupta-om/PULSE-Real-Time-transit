# calendar_widget.py - Sleek Cyberpunk Clock & Technical Cyan Calendar

import datetime
import streamlit as st
import streamlit.components.v1 as components

def render_technical_sidebar_calendar():
    """
    Renders a glowing technical digital clock HUD and an integrated cyan-accent calendar.
    """
    now = datetime.datetime.now()
    current_date_str = now.strftime("%a, %d %b %Y").upper()

    st.sidebar.markdown("---")

    # 1. Clean Cyberpunk HUD Digital Clock (Transparent & Glowing)
    clock_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            }}
            .hud-clock-card {{
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(0, 229, 255, 0.4);
                border-radius: 12px;
                padding: 8px 18px;
                text-align: center;
                box-shadow: 0 0 15px rgba(0, 229, 255, 0.15);
                width: 85%;
            }}
            .time-display {{
                font-family: 'Courier New', Courier, monospace;
                font-size: 20px;
                font-weight: 900;
                color: #00e5ff;
                text-shadow: 0 0 10px rgba(0, 229, 255, 0.8);
                letter-spacing: 2px;
            }}
            .date-display {{
                font-size: 10px;
                color: #94a3b8;
                margin-top: 2px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
        </style>
        <script>
            function updateClock() {{
                var now = new Date();
                var timeStr = now.toLocaleTimeString();
                document.getElementById('clock').innerHTML = timeStr;
                setTimeout(updateClock, 1000);
            }}
        </script>
    </head>
    <body onload="updateClock()">
        <div class="hud-clock-card">
            <div class="time-display" id="clock">--:--:--</div>
            <div class="date-display">⚡ {current_date_str}</div>
        </div>
    </body>
    </html>
    """
    components.html(clock_html, height=65)

    # 2. Technical Cyan CSS Styling for Streamlit Calendar Date Picker
    st.markdown(
        """
        <style>
            /* Customizing Streamlit Date Picker to Match App Tech Theme */
            div[data-baseweb="datepicker"] {
                background-color: rgba(15, 23, 42, 0.8) !important;
                border: 1px solid rgba(0, 229, 255, 0.3) !important;
                border-radius: 10px !important;
            }
            /* Change Red highlight to Cyan Accent */
            div[data-baseweb="calendar"] button[aria-selected="true"] {
                background-color: #00e5ff !important;
                color: #020617 !important;
                font-weight: bold !important;
                border-radius: 50% !important;
            }
            /* Calendar Header styling */
            div[aria-label="Calendar"] {
                background-color: #0f172a !important;
                border-radius: 12px !important;
                border: 1px solid rgba(255,255,255,0.1) !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("##### 📅 Schedule Calendar")
    
    if 'selected_calendar_date' not in st.session_state:
        st.session_state.selected_calendar_date = datetime.date.today()

    user_selected_date = st.sidebar.date_input(
        label="Select Date / Month:",
        value=st.session_state.selected_calendar_date,
        key="interactive_transit_calendar"
    )

    st.session_state.selected_calendar_date = user_selected_date