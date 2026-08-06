# weather_fx.py - Premium Glassmorphism Weather FX Engine

import streamlit as st

def render_weather_background(weather_status, is_monsoon_active, source_station=""):
    """
    Renderslocation-aware weather FX using Glassmorphism styling and high-visibility particle effects.
    """
    status_lower = str(weather_status).lower()
    
    # Check if user explicitly activated monsoon OR it's a known rain-heavy location
    is_rain_active = is_monsoon_active or ("rain" in status_lower and "light" not in status_lower)
    
    # 🌧️ Premium Neon Blue Rain Effect
    if is_rain_active:
        css = """
        <style>
            .stApp {
                background: linear-gradient(135deg, #0b131e 0%, #111a28 100%) !important;
            }
            .rain-container {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                pointer-events: none; z-index: 0; overflow: hidden;
            }
            .rain-drop {
                position: absolute;
                background: linear-gradient(to bottom, rgba(77, 166, 255, 0), rgba(77, 166, 255, 0.75));
                width: 2px; height: 60px; border-radius: 2px;
                animation: dropFall 0.7s linear infinite;
            }
            @keyframes dropFall {
                0% { transform: translateY(-70px); opacity: 1; }
                85% { opacity: 0.8; }
                100% { transform: translateY(100vh); opacity: 0; }
            }
        </style>
        <div class="rain-container">
            <div class="rain-drop" style="left: 5%; animation-duration: 0.55s; animation-delay: 0s;"></div>
            <div class="rain-drop" style="left: 15%; animation-duration: 0.65s; animation-delay: 0.2s;"></div>
            <div class="rain-drop" style="left: 28%; animation-duration: 0.5s; animation-delay: 0.4s;"></div>
            <div class="rain-drop" style="left: 42%; animation-duration: 0.72s; animation-delay: 0.1s;"></div>
            <div class="rain-drop" style="left: 58%; animation-duration: 0.58s; animation-delay: 0.3s;"></div>
            <div class="rain-drop" style="left: 71%; animation-duration: 0.68s; animation-delay: 0.15s;"></div>
            <div class="rain-drop" style="left: 85%; animation-duration: 0.52s; animation-delay: 0.35s;"></div>
            <div class="rain-drop" style="left: 95%; animation-duration: 0.62s; animation-delay: 0.05s;"></div>
        </div>
        """
    # ☁️ Moving Clouds Effect (Default for Light Showers / Overcast)
    elif "cloud" in status_lower or "shower" in status_lower or "drizzle" in status_lower:
        css = """
        <style>
            .stApp {
                background: linear-gradient(135deg, #101726 0%, #1a2333 100%) !important;
            }
            .cloud-layer {
                position: fixed; top: 15px; left: 0; width: 100vw; height: 180px;
                pointer-events: none; z-index: 0; opacity: 0.18; overflow: hidden;
            }
            .cloud-shape {
                position: absolute; background: #ffffff; border-radius: 100px;
                width: 220px; height: 60px; animation: moveCloud 35s linear infinite;
            }
            .cloud-shape::before {
                content: ''; position: absolute; top: -25px; left: 30px;
                width: 90px; height: 90px; background: #ffffff; border-radius: 50%;
            }
            @keyframes moveCloud {
                0% { transform: translateX(-250px); }
                100% { transform: translateX(100vw); }
            }
        </style>
        <div class="cloud-layer">
            <div class="cloud-shape" style="top: 10px; animation-duration: 40s;"></div>
            <div class="cloud-shape" style="top: 60px; animation-duration: 28s; animation-delay: -12s; scale: 0.75;"></div>
        </div>
        """
    # ☀️ Clean Dark Mode (Default)
    else:
        css = """
        <style>
            .stApp {
                background: linear-gradient(135deg, #0e1726 0%, #030712 100%) !important;
            }
        </style>
        """
    
    st.markdown(css, unsafe_allow_html=True)