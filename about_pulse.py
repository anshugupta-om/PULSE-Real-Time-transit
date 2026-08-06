# about_pulse.py - Balanced Cyber-UI About Module with Value Impact Focus

import streamlit as st

def inject_about_css():
    st.markdown("""
    <style>
    /* ---------------------------------------------------------
       1. ANIMATIONS & EFFECTS
    --------------------------------------------------------- */
    @keyframes titleGradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes neonGlow {
        0% { border-color: rgba(0, 229, 255, 0.4); box-shadow: 0 0 12px rgba(0, 229, 255, 0.2); }
        50% { border-color: rgba(168, 85, 247, 0.6); box-shadow: 0 0 20px rgba(168, 85, 247, 0.3); }
        100% { border-color: rgba(0, 229, 255, 0.4); box-shadow: 0 0 12px rgba(0, 229, 255, 0.2); }
    }

    /* ---------------------------------------------------------
       2. TYPOGRAPHY & HERO STYLING
    --------------------------------------------------------- */
    .about-hero-title {
        font-size: 38px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00e5ff, #a855f7, #ec4899, #00e5ff);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: titleGradientShift 6s ease infinite;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }

    .about-hero-sub {
        font-size: 15px;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 35px;
        font-weight: 500;
    }

    /* ---------------------------------------------------------
       3. BALANCED SYMMETRICAL CARDS
    --------------------------------------------------------- */
    .feature-card {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 229, 255, 0.25);
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-6px);
        border-color: #00e5ff;
        box-shadow: 0 18px 35px rgba(0, 229, 255, 0.25);
    }

    .team-card-balanced {
        background: rgba(15, 23, 42, 0.88);
        backdrop-filter: blur(18px);
        border: 1.5px solid rgba(0, 229, 255, 0.4);
        border-radius: 22px;
        padding: 26px;
        animation: neonGlow 4s infinite alternate;
        transition: transform 0.3s ease;
    }

    .team-card-balanced:hover {
        transform: translateY(-6px);
    }

    .role-badge-cyan {
        display: inline-block;
        background: linear-gradient(90deg, #00e5ff 0%, #a855f7 100%);
        color: #020617;
        font-weight: 900;
        font-size: 11px;
        padding: 5px 14px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 12px;
    }

    .role-badge-purple {
        display: inline-block;
        background: linear-gradient(90deg, #a855f7 0%, #ec4899 100%);
        color: #ffffff;
        font-weight: 900;
        font-size: 11px;
        padding: 5px 14px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 12px;
    }

    .team-name {
        font-size: 25px;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .team-desc {
        font-size: 14px;
        color: #cbd5e1;
        line-height: 1.6;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

def render_about_page():
    inject_about_css()

    st.markdown('<div class="about-hero-title">Inside PULSE: Next-Gen Mumbai Transit System</div>', unsafe_allow_html=True)
    st.markdown('<div class="about-hero-sub">Real-Time Transit Tracking, Commuter Safety & Smart AI Intelligence</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SECTION 1: CORE CAPABILITIES
    # ---------------------------------------------------------
    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color:#00e5ff; margin-top:0; font-size:18px;">⚡ Live Tracking</h4>
            <p style="color:#94a3b8; font-size:13.5px; margin:0;">Real-time GPS telemetry, crowd density predictions, and dynamic route ETAs across Western & Central lines.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_v2:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color:#a855f7; margin-top:0; font-size:18px;">🛡️ Commuter Safety</h4>
            <p style="color:#94a3b8; font-size:13.5px; margin:0;">Instant SOS triggers, silent RPF alerts, and offline zero-network emergency siren modes.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_v3:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color:#ec4899; margin-top:0; font-size:18px;">🤖 Pulse Buddy AI</h4>
            <p style="color:#94a3b8; font-size:13.5px; margin:0;">Interactive mascot assistant providing instant route guidance, tickets, and helpline alerts.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SECTION 2: BALANCED TEAM CREDITS
    # ---------------------------------------------------------
    st.markdown("### 👥 Project Team & Leadership")
    
    t_col1, t_col2 = st.columns(2)

    with t_col1:
        st.markdown("""
        <div class="team-card-balanced">
            <span class="role-badge-cyan">👑 Project Lead & Core Initiator</span>
            <div class="team-name">Mili Srivastava</div>
            <p class="team-desc">
                Lead developer responsible for end-to-end design, implementation, AI integration, and complete system execution of Project PULSE.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with t_col2:
        st.markdown("""
        <div class="team-card-balanced">
            <span class="role-badge-purple">💡 Concept Contributor</span>
            <div class="team-name">Anshu Gupta</div>
            <p class="team-desc">
                Contributed the initial idea and problem statement regarding Metro transit convenience.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SECTION 3: VALUE IMPACT (COMMUTER BENEFIT FOCUS)
    # ---------------------------------------------------------
    with st.expander("🌟 Why PULSE is Essential for Everyday Commuters"):
        st.markdown("""
        * ⏱️ **Saves 15-20 Minutes Daily:** Eliminates platform confusion by suggesting coaches with lower crowding density.
        * 🛡️ **24x7 Underground Protection:** Ensures passenger safety even in underground tunnels with zero network connectivity.
        * 📲 **One-Tap Help Access:** Instant access to ticketing guidelines, route switches, and official railway police support.
        * 📊 **Authority Telemetry:** Real-time logging enables swift action during unexpected transit disruptions or medical emergencies.
        """)