# copilot_engine.py - AURA: Animated Expressions & Stable Spacing Layout

import random
import streamlit as st
import streamlit.components.v1 as components

def render_safety_copilot(source, destination, overall_density, live_weather_status):
    st.markdown("---")
    
    override_mood = st.session_state.get('aura_mood_override', None)
    username = st.session_state.get('username', 'Commuter')

    # 🎭 Dynamic Expression Arrays & Animations
    if override_mood == "HAPPY" or (not override_mood and overall_density < 35):
        mood_title = "HAPPY & WELCOMING"
        status_color = "#00e676"
        left_arm_animation = "animation: armWave 1.8s ease-in-out infinite;"
        right_arm_animation = ""
        head_animation = "animation: headTilt 3s ease-in-out infinite;"
        
        # Eyes SVG for Happy (Curved & Blinking)
        eyes_svg_code = """
        <svg width="70" height="40" viewBox="0 0 70 40" class="blinking-eyes">
            <path d="M 12,25 Q 22,10 32,25" stroke="#00e676" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M 38,25 Q 48,10 58,25" stroke="#00e676" stroke-width="5" fill="none" stroke-linecap="round"/>
        </svg>
        """
        clean_voice_text = f"Beep Boop! Welcome {username}! Platform at {source} is peaceful and clear. Have a wonderful ride!"
        speech_text = f"Beep Boop! Welcome {username}! Platform at <b>{source}</b> is peaceful and clear. Have a wonderful ride!"

    elif override_mood == "ALERT" or (not override_mood and overall_density < 65):
        mood_title = "ALERT & MONITORING"
        status_color = "#ffb74d"
        left_arm_animation = ""
        right_arm_animation = ""
        head_animation = "animation: headScan 2.5s ease-in-out infinite;"
        
        # Eyes SVG for Alert (Focused Cameras Blinking)
        eyes_svg_code = """
        <svg width="70" height="40" viewBox="0 0 70 40" class="blinking-eyes">
            <circle cx="22" cy="20" r="8" fill="#ffb74d"/>
            <circle cx="48" cy="20" r="8" fill="#ffb74d"/>
        </svg>
        """
        clean_voice_text = f"Scanning telemetry. Crowd density at {source} is steady at {overall_density} percent. I recommend walking towards Coach C2 or C11."
        speech_text = f"Scanning telemetry... Crowd density at <b>{source}</b> is steady ({overall_density}%). I recommend walking towards <b>Coach C2 or C11</b>."

    else:  # Worried / High Density
        mood_title = "WORRIED / HIGH DENSITY"
        status_color = "#ff1744"
        left_arm_animation = "animation: armWorry 0.8s ease-in-out infinite;"
        right_arm_animation = "animation: armWorry 0.8s ease-in-out infinite alternate;"
        head_animation = "animation: headTremble 0.6s ease-in-out infinite;"
        
        # Eyes SVG for Worried (Crossed Alarm Eyes)
        eyes_svg_code = """
        <svg width="70" height="40" viewBox="0 0 70 40" class="blinking-eyes">
            <path d="M 12,12 L 28,28 M 28,12 L 12,28" stroke="#ff1744" stroke-width="5" stroke-linecap="round"/>
            <path d="M 42,12 L 58,28 M 58,12 L 42,28" stroke="#ff1744" stroke-width="5" stroke-linecap="round"/>
        </svg>
        """
        clean_voice_text = f"Warning! High crowd density detected at {source}, {overall_density} percent. Please stay back from the platform edge and take Coach C1 or C12."
        speech_text = f"Oh no! High crowd density detected at <b>{source}</b> ({overall_density}%)! Please stay back from the platform edge and take end coaches <b>C1 or C12</b>."

    st.markdown("### 🤖 MEET AURA: Humanoid AI Safety Companion")
    st.caption("AURA is an interactive humanoid companion that uses body gestures, LED eye expressions, and voice feedback.")

    h_col1, h_col2 = st.columns([1.1, 2.5])

    with h_col1:
        robot_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    padding-top: 5px;
                    background: transparent;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    font-family: system-ui, -apple-system, sans-serif;
                }}
                @keyframes eyeBlink {{
                    0%, 90%, 100% {{ opacity: 1; transform: scaleY(1); }}
                    95% {{ opacity: 0.2; transform: scaleY(0.1); }}
                }}
                .blinking-eyes {{
                    animation: eyeBlink 3.5s infinite;
                    transform-origin: center;
                }}
                @keyframes floatRobot {{
                    0%, 100% {{ transform: translateY(0px); }}
                    50% {{ transform: translateY(-6px); }}
                }}
                @keyframes armWave {{
                    0%, 100% {{ transform: rotate(0deg); }}
                    50% {{ transform: rotate(-35deg); }}
                }}
                @keyframes armWorry {{
                    0%, 100% {{ transform: translateY(0px) rotate(10deg); }}
                    50% {{ transform: translateY(-8px) rotate(-15deg); }}
                }}
                @keyframes headTilt {{
                    0%, 100% {{ transform: rotate(0deg); }}
                    50% {{ transform: rotate(4deg); }}
                }}
                @keyframes headScan {{
                    0%, 100% {{ transform: translateX(0px); }}
                    50% {{ transform: translateX(6px); }}
                }}
                @keyframes headTremble {{
                    0%, 100% {{ transform: translateY(0px); }}
                    50% {{ transform: translateY(-2px); }}
                }}
                .robot-container {{
                    animation: floatRobot 3.5s ease-in-out infinite;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
                .robot-head {{
                    width: 135px;
                    height: 105px;
                    background: linear-gradient(145deg, #f1f5f9, #94a3b8);
                    border-radius: 38px 38px 28px 28px;
                    position: relative;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.45);
                    border: 2px solid #cbd5e1;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 2;
                    {head_animation}
                }}
                .robot-visor {{
                    width: 105px;
                    height: 75px;
                    background: #020617;
                    border-radius: 22px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border: 2.5px solid {status_color};
                    box-shadow: 0 0 14px {status_color};
                }}
                .robot-torso {{
                    width: 100px;
                    height: 68px;
                    background: linear-gradient(145deg, #cbd5e1, #64748b);
                    border-radius: 18px 18px 32px 32px;
                    margin-top: -9px;
                    position: relative;
                    box-shadow: 0 8px 18px rgba(0,0,0,0.35);
                    border: 2px solid #94a3b8;
                    z-index: 1;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .core-badge {{
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    background: #020617;
                    border: 2px solid {status_color};
                    box-shadow: 0 0 10px {status_color};
                }}
                .left-arm, .right-arm {{
                    width: 20px;
                    height: 50px;
                    background: linear-gradient(145deg, #94a3b8, #475569);
                    border-radius: 10px;
                    position: absolute;
                    top: 6px;
                    border: 1px solid #cbd5e1;
                }}
                .left-arm {{ left: -15px; transform-origin: top right; {left_arm_animation} }}
                .right-arm {{ right: -15px; transform-origin: top left; {right_arm_animation} }}
                .status-title {{
                    margin-top: 8px;
                    font-weight: 800;
                    color: {status_color};
                    font-size: 12px;
                    letter-spacing: 1px;
                }}
            </style>
        </head>
        <body>
            <div class="robot-container">
                <div class="robot-head">
                    <div class="robot-visor">
                        {eyes_svg_code}
                    </div>
                </div>
                <div class="robot-torso">
                    <div class="left-arm"></div>
                    <div class="core-badge"></div>
                    <div class="right-arm"></div>
                </div>
                <div class="status-title">● {mood_title}</div>
            </div>
        </body>
        </html>
        """
        components.html(robot_html, height=230)

    with h_col2:
        st.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(14px); border-radius: 20px; padding: 22px; border: 1px solid rgba(255,255,255,0.1); border-left: 5px solid {status_color}; box-shadow: 0 12px 30px rgba(0,0,0,0.4); min-height: 145px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {status_color}; font-size: 17px;">💬 AURA Telemetry Voice Advisory</h4>
                    <p style="color: #e2e8f0; font-size: 15px; line-height: 1.6; margin: 0;">
                        {speech_text}
                    </p>
                </div>
                <div style="margin-top: 15px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                    <span style="background: rgba(0, 229, 255, 0.1); border: 1px solid #00e5ff; color: #00e5ff; padding: 6px 14px; border-radius: 8px; font-size: 12px; font-weight: bold;">
                        🛡️ Safe Boarding: Coach C1 / C12
                    </span>
                    <span style="background: rgba(179, 136, 255, 0.1); border: 1px solid #b388ff; color: #b388ff; padding: 6px 14px; border-radius: 8px; font-size: 12px; font-weight: bold;">
                        📡 Telemetry 100% Synced
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        components.html(
            f"""
            <script>
                function speakAuraText() {{
                    if ('speechSynthesis' in window) {{
                        window.speechSynthesis.cancel();
                        var msg = new SpeechSynthesisUtterance("{clean_voice_text}");
                        msg.rate = 0.95;
                        msg.pitch = 1.25;
                        window.speechSynthesis.speak(msg);
                    }}
                }}
            </script>
            <button onclick="speakAuraText()" style="
                background: linear-gradient(135deg, {status_color}, #00b0ff);
                border: none;
                color: #020617;
                padding: 10px 20px;
                border-radius: 12px;
                cursor: pointer;
                font-weight: bold;
                font-size: 13px;
                margin-top: 10px;
                box-shadow: 0 4px 15px rgba(0,229,255,0.3);
                width: 100%;
            ">🔊 Tap to Hear AURA Speak Out Loud</button>
            """,
            height=60
        )

    st.markdown("---")
    with st.expander("🎮 Humanoid Robot Pose & Expression Controls"):
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)
        
        if p_col1.button("👋 Wave & Happy Pose", width="stretch"):
            st.session_state.aura_mood_override = "HAPPY"
            st.rerun()
        if p_col2.button("🧐 Focused Alert Pose", width="stretch"):
            st.session_state.aura_mood_override = "ALERT"
            st.rerun()
        if p_col3.button("😰 Worried Gesture Pose", width="stretch"):
            st.session_state.aura_mood_override = "WORRIED"
            st.rerun()
        if p_col4.button("🔄 Auto Telemetry Mode", width="stretch"):
            st.session_state.aura_mood_override = None
            st.rerun()