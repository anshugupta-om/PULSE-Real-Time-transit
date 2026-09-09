# global_theme.py
# PULSE - Global Responsive Theme & UI CSS

import streamlit as st


def init_theme():
    """Initialize PULSE theme."""

    if "theme" not in st.session_state:
        st.session_state.theme = "Default"


def render_theme_selector():
    """Render global theme selector."""

    init_theme()

    themes = ["Default", "Dark", "Light"]

    selected = st.sidebar.selectbox(
        "🎨 Theme",
        themes,
        index=themes.index(st.session_state.theme),
        key="global_pulse_theme"
    )

    if selected != st.session_state.theme:
        st.session_state.theme = selected
        st.rerun()


def apply_global_css():
    """
    Apply global responsive CSS to the complete PULSE application.

    Default = original PULSE theme.
    Dark   = dark theme.
    Light  = light theme.
    """

    init_theme()

    theme = st.session_state.theme

    # ==========================================================
    # DEFAULT COLORS
    # ==========================================================

    if theme == "Default":

        bg = "#0b1220"
        card = "#111827"
        card2 = "#172033"
        text = "#f8fafc"
        secondary = "#cbd5e1"
        muted = "#94a3b8"
        border = "rgba(148, 163, 184, 0.20)"
        input_bg = "#1e293b"

    # ==========================================================
    # DARK
    # ==========================================================

    elif theme == "Dark":

        bg = "#020617"
        card = "#0f172a"
        card2 = "#1e293b"
        text = "#ffffff"
        secondary = "#e2e8f0"
        muted = "#94a3b8"
        border = "rgba(148, 163, 184, 0.25)"
        input_bg = "#1e293b"

    # ==========================================================
    # LIGHT
    # ==========================================================

    else:

        bg = "#f1f5f9"
        card = "#ffffff"
        card2 = "#f8fafc"
        text = "#0f172a"
        secondary = "#334155"
        muted = "#64748b"
        border = "#cbd5e1"
        input_bg = "#ffffff"

    # ==========================================================
    # GLOBAL CSS
    # ==========================================================

    st.markdown(
        f"""
        <style>

        /* =====================================================
           GLOBAL VARIABLES
        ===================================================== */

        :root {{
            --pulse-bg: {bg};
            --pulse-card: {card};
            --pulse-card-2: {card2};
            --pulse-text: {text};
            --pulse-text-secondary: {secondary};
            --pulse-text-muted: {muted};
            --pulse-border: {border};
            --pulse-input: {input_bg};
            --pulse-accent: #00d9ff;
        }}


        /* =====================================================
           MAIN APPLICATION
        ===================================================== */

        /* NOTE: background here intentionally has no !important so that  */
        /* page-specific CSS (e.g. the auth background image) can override. */
        .stApp {{
            background: var(--pulse-bg);
            color: var(--pulse-text) !important;
        }}

        [data-testid="stAppViewContainer"] {{
            background: var(--pulse-bg);
            color: var(--pulse-text) !important;
        }}

        [data-testid="stMain"] {{
            background: var(--pulse-bg);
            color: var(--pulse-text) !important;
        }}


        /* =====================================================
           GLOBAL TEXT
        ===================================================== */

        body,
        p,
        span,
        label,
        div,
        li,
        td,
        th {{
            color: var(--pulse-text);
        }}

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {{
            color: var(--pulse-text) !important;
        }}

        [data-testid="stMarkdownContainer"] {{
            color: var(--pulse-text) !important;
        }}

        [data-testid="stMarkdownContainer"] p {{
            color: var(--pulse-text) !important;
        }}


        /* =====================================================
           SIDEBAR
        ===================================================== */

        [data-testid="stSidebar"] {{
            background: var(--pulse-card) !important;
            border-right: 1px solid var(--pulse-border) !important;
        }}

        [data-testid="stSidebar"] * {{
            color: var(--pulse-text) !important;
        }}


        /* =====================================================
           INPUTS
        ===================================================== */

        input,
        textarea {{
            background: var(--pulse-input) !important;
            color: var(--pulse-text) !important;
            border: 1px solid var(--pulse-border) !important;
        }}

        input::placeholder,
        textarea::placeholder {{
            color: var(--pulse-text-muted) !important;
        }}


        


        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton > button {{
            background: var(--pulse-card-2) !important;
            color: var(--pulse-text) !important;
            border: 1px solid var(--pulse-border) !important;
            border-radius: 8px !important;
        }}

        .stButton > button:hover {{
            border-color: var(--pulse-accent) !important;
            color: var(--pulse-accent) !important;
        }}


        /* =====================================================
           METRICS
        ===================================================== */

        [data-testid="stMetric"] {{
            background: var(--pulse-card) !important;
            border: 1px solid var(--pulse-border) !important;
            border-radius: 12px !important;
            padding: 12px !important;
        }}

        [data-testid="stMetricLabel"] {{
            color: var(--pulse-text-secondary) !important;
        }}

        [data-testid="stMetricValue"] {{
            color: var(--pulse-text) !important;
        }}

        [data-testid="stMetricDelta"] {{
            color: var(--pulse-text-secondary) !important;
        }}


        /* =====================================================
           EXPANDERS
        ===================================================== */

        [data-testid="stExpander"] {{
            background: var(--pulse-card) !important;
            border: 1px solid var(--pulse-border) !important;
            color: var(--pulse-text) !important;
        }}

        [data-testid="stExpander"] * {{
            color: var(--pulse-text) !important;
        }}


        /* =====================================================
           ALERTS
        ===================================================== */

        [data-testid="stAlert"] {{
            border-radius: 10px !important;
        }}


        /* =====================================================
           DATAFRAME / TABLE
        ===================================================== */

        [data-testid="stDataFrame"] {{
            background: var(--pulse-card) !important;
        }}

        table {{
            color: var(--pulse-text) !important;
        }}

        th {{
            color: var(--pulse-text) !important;
            background: var(--pulse-card-2) !important;
        }}

        td {{
            color: var(--pulse-text) !important;
        }}


        /* =====================================================
           DIVIDERS
        ===================================================== */

        hr {{
            border-color: var(--pulse-border) !important;
        }}


        /* =====================================================
           LINKS
        ===================================================== */

        a {{
            color: var(--pulse-accent) !important;
        }}


        /* =====================================================
           ROUTE RECOMMENDER
        ===================================================== */

        .pulse-route-card {{
            background: var(--pulse-card) !important;
            color: var(--pulse-text) !important;
            border: 1px solid var(--pulse-border) !important;
            border-radius: 14px !important;
        }}

        .pulse-route-card * {{
            color: var(--pulse-text) !important;
        }}


        /* =====================================================
           MOBILE RESPONSIVENESS
        ===================================================== */

        @media screen and (max-width: 768px) {{

            /* Prevent horizontal overflow */

            .stApp {{
                width: 100% !important;
                overflow-x: hidden !important;
            }}

            [data-testid="stMain"] {{
                width: 100% !important;
                overflow-x: hidden !important;
            }}


            /* Mobile text */

            h1 {{
                font-size: 1.7rem !important;
                color: var(--pulse-text) !important;
            }}

            h2 {{
                font-size: 1.4rem !important;
                color: var(--pulse-text) !important;
            }}

            h3 {{
                font-size: 1.2rem !important;
                color: var(--pulse-text) !important;
            }}

            h4 {{
                font-size: 1.05rem !important;
                color: var(--pulse-text) !important;
            }}

            p {{
                font-size: 0.95rem !important;
                color: var(--pulse-text) !important;
            }}


            /* Mobile markdown */

            [data-testid="stMarkdownContainer"] {{
                color: var(--pulse-text) !important;
            }}

            [data-testid="stMarkdownContainer"] p {{
                color: var(--pulse-text) !important;
            }}


            /* Mobile metrics */

            [data-testid="stMetric"] {{
                padding: 10px !important;
            }}

            [data-testid="stMetricLabel"] {{
                color: var(--pulse-text-secondary) !important;
            }}

            [data-testid="stMetricValue"] {{
                color: var(--pulse-text) !important;
                font-size: 1.25rem !important;
            }}


            /* Mobile buttons */

            .stButton > button {{
                width: 100% !important;
                min-height: 42px !important;
            }}


            /* Mobile inputs */

            input,
            textarea {{
                font-size: 16px !important;
            }}


            /* Mobile containers */

            [data-testid="stVerticalBlock"] {{
                max-width: 100% !important;
            }}

        }}


        /* =====================================================
           EXTRA SMALL PHONES
        ===================================================== */

        @media screen and (max-width: 480px) {{

            h1 {{
                font-size: 1.45rem !important;
            }}

            h2 {{
                font-size: 1.25rem !important;
            }}

            h3 {{
                font-size: 1.1rem !important;
            }}

            p {{
                font-size: 0.9rem !important;
            }}

            [data-testid="stMetricValue"] {{
                font-size: 1.1rem !important;
            }}

        }}

        </style>
        """,
        unsafe_allow_html=True
    )