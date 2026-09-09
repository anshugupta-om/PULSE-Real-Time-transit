# route_recommender.py
# PULSE Intelligent Route Recommendation Engine

import streamlit as st


def calculate_route_score(eta, crowd, cost):
    """
    Higher score = better route.

    Factors:
    - ETA   : 40%
    - Crowd : 40%
    - Cost  : 20%
    """

    # Lower ETA = better score
    eta_score = max(0, 100 - (eta * 2))

    # Lower crowd = better score
    crowd_score = 100 - crowd

    # Lower cost = better score
    cost_score = max(0, 100 - (cost * 1.5))

    final_score = (
        eta_score * 0.40
        + crowd_score * 0.40
        + cost_score * 0.20
    )

    return round(final_score, 1)


def get_route_candidates(
    source,
    destination,
    selected_line,
    crowd_density,
    weather_status
):
    """
    Generates alternative route options.

    These are recommendation scenarios based on
    current PULSE data.

    They are not live railway schedules.
    """

    # =================================================
    # ROUTE 1 - CURRENT LOCAL ROUTE
    # =================================================

    local_eta = 35

    if crowd_density >= 70:
        local_eta += 10

    elif crowd_density >= 50:
        local_eta += 5

    local_crowd = crowd_density

    local_cost = 20

    # =================================================
    # ROUTE 2 - BUS + ALTERNATE TRANSIT
    # =================================================

    alternate_eta = 25

    # Rain can increase alternate transit travel time
    if weather_status == "Light Showers/Rain":
        alternate_eta += 5

    alternate_crowd = max(
        20,
        crowd_density - 25
    )

    alternate_cost = 45

    # =================================================
    # ROUTE 3 - FEEDER + SHARED MOBILITY
    # =================================================

    feeder_eta = 30

    if crowd_density >= 70:
        feeder_eta -= 3

    feeder_crowd = max(
        15,
        crowd_density - 35
    )

    feeder_cost = 55

    # =================================================
    # CREATE ROUTES
    # =================================================

    routes = [

        {
            "name": "Current Local Route",
            "type": "🚆 Local Train",
            "eta": local_eta,
            "crowd": local_crowd,
            "cost": local_cost
        },

        {
            "name": "Bus + Alternate Transit",
            "type": "🚌 Bus + Metro",
            "eta": alternate_eta,
            "crowd": alternate_crowd,
            "cost": alternate_cost
        },

        {
            "name": "Feeder + Shared Mobility",
            "type": "🚌 Feeder + Auto",
            "eta": feeder_eta,
            "crowd": feeder_crowd,
            "cost": feeder_cost
        }

    ]

    # =================================================
    # CALCULATE ROUTE SCORE
    # =================================================

    for route in routes:

        route["score"] = calculate_route_score(
            route["eta"],
            route["crowd"],
            route["cost"]
        )

    # Highest score first
    routes.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return routes



def render_route_recommendation(
    source,
    destination,
    selected_line,
    crowd_density,
    weather_status
):
    """
    Displays the PULSE Intelligent Route Recommendation.
    """

    st.markdown(
        """
        <style>

        /* =====================================================
           PULSE ROUTE RECOMMENDER - RESPONSIVE TEXT FIX
           ===================================================== */

        [data-testid="stAppViewContainer"] {
            color: #f8fafc;
        }

        h3,
        h4 {
            color: #f8fafc !important;
        }

        [data-testid="stMarkdownContainer"] p {
            color: #f8fafc !important;
        }

        [data-testid="stCaptionContainer"] {
            color: #cbd5e1 !important;
        }

        [data-testid="stMetricLabel"] {
            color: #cbd5e1 !important;
        }

        [data-testid="stMetricValue"] {
            color: #f8fafc !important;
        }

        [data-testid="stMetricDelta"] {
            color: #cbd5e1 !important;
        }

        @media screen and (max-width: 768px) {

            [data-testid="stAppViewContainer"] {
                background: #0f172a !important;
                color: #f8fafc !important;
            }

            h3,
            h4,
            h5 {
                color: #f8fafc !important;
            }

            [data-testid="stMarkdownContainer"] p {
                color: #f8fafc !important;
            }

            [data-testid="stCaptionContainer"] {
                color: #cbd5e1 !important;
            }

            [data-testid="stMetricLabel"] {
                color: #cbd5e1 !important;
            }

            [data-testid="stMetricValue"] {
                color: #ffffff !important;
            }

            [data-testid="stMetricDelta"] {
                color: #cbd5e1 !important;
            }

            [data-testid="stVerticalBlock"] {
                color: #f8fafc !important;
            }

            .stMarkdown {
                color: #f8fafc !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    routes = get_route_candidates(
        source,
        destination,
        selected_line,
        crowd_density,
        weather_status
    )

    
    routes = get_route_candidates(
        source,
        destination,
        selected_line,
        crowd_density,
        weather_status
    )

    best_route = routes[0]

    # =================================================
    # HEADER
    # =================================================

    st.markdown("---")

    st.markdown(
        "### 🧠 PULSE Intelligent Route Recommendation"
    )

    st.caption(
        f"Optimizing route from **{source}** to **{destination}** "
        f"using ETA, crowd, cost and weather conditions."
    )

    # =================================================
    # BEST ROUTE
    # =================================================

    st.success(
        f"🏆 Recommended Route: **{best_route['name']}**"
    )

    best_col1, best_col2, best_col3, best_col4 = st.columns(4)

    with best_col1:

        st.metric(
            "⏱️ ETA",
            f"{best_route['eta']} min"
        )

    with best_col2:

        st.metric(
            "👥 Crowd",
            f"{best_route['crowd']}%"
        )

    with best_col3:

        st.metric(
            "💰 Cost",
            f"₹{best_route['cost']}"
        )

    with best_col4:

        st.metric(
            "⭐ Route Score",
            f"{best_route['score']}/100"
        )

    # =================================================
    # ROUTE COMPARISON
    # =================================================

    st.markdown("#### 🔍 Route Comparison")

    for index, route in enumerate(routes):

        if index == 0:
            status = "🏆 BEST"
        else:
            status = "Alternative"

        with st.container(border=True):

            c1, c2, c3, c4, c5 = st.columns(5)

            with c1:

                st.write(
                    f"**{status}**"
                )

            with c2:

                st.write(
                    route["type"]
                )

            with c3:

                st.write(
                    f"⏱️ {route['eta']} min"
                )

            with c4:

                st.write(
                    f"👥 {route['crowd']}%"
                )

            with c5:

                st.write(
                    f"⭐ {route['score']}/100"
                )

    # =================================================
    # WHY THIS ROUTE?
    # =================================================

    st.markdown(
        "#### 💡 Why PULSE selected this route"
    )

    reasons = []

    # Fast route
    if best_route["eta"] <= 25:

        reasons.append(
            "⚡ Fast travel time"
        )

    # Lower crowd
    if best_route["crowd"] < crowd_density:

        reasons.append(
            f"👥 Lower crowd than current route "
            f"({crowd_density}%)"
        )

    # Weather
    if weather_status == "Light Showers/Rain":

        reasons.append(
            "🌧️ Current weather conditions considered"
        )

    # Cost
    if best_route["cost"] <= 30:

        reasons.append(
            "💰 Lower travel cost"
        )

    # If no specific reason
    if not reasons:

        reasons.append(
            "Balanced combination of travel time, "
            "crowd and cost."
        )

    # Display reasons
    for reason in reasons:

        st.write(
            f"✓ {reason}"
        )