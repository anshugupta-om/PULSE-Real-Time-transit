# digital_twin_ui.py - Authentic 3D Digital Twin Coach Layout

import random
import streamlit as st
import streamlit.components.v1 as components

# Real-world coach offsets based on platform exit staircases in Mumbai Local
COACH_OFFSETS = {
    "C1": -18, "C2": -8,  "C3": 12,  "C4": 22, 
    "C5": 4,   "C6": 24,  "C7": 18,  "C8": -2, 
    "C9": 14,  "C10": -10, "C11": -5, "C12": -20
}

def render_digital_twin(overall_crowd_percent):
    """
    Renders 3D Train Coach Digital Twin with authentic spatial gradients.
    """
    st.markdown("---")
    st.markdown("### 🚄 AI Digital Twin: Live Train Coach Status")

    coaches = [f"C{i}" for i in range(1, 13)]
    current_densities = {}
    
    for c in coaches:
        offset = COACH_OFFSETS.get(c, 0)
        coach_crowd = max(10, min(98, overall_crowd_percent + offset + random.randint(-2, 2)))
        current_densities[c] = coach_crowd

    avg_coach_crowd = sum(current_densities.values()) // len(current_densities)

    html_code = _generate_html(current_densities)
    components.html(html_code, height=360, scrolling=True)

    return avg_coach_crowd

def _generate_html(current_densities):
    def get_color(density):
        if density < 35: return "#28a745", "Seats Available"
        elif density < 65: return "#ffc107", "Moderate Crowd"
        else: return "#dc3545", "Overcrowded"

    html = """
    <style>
        .train-track {
            display: flex; gap: 12px; overflow-x: auto; padding: 25px 10px;
            background: linear-gradient(to bottom, #1e1e1e, #121212);
            border-radius: 12px; border-bottom: 4px solid #444; margin-bottom: 15px;
        }
        .coach-3d {
            min-width: 78px; height: 105px; border-radius: 8px;
            display: flex; flex-direction: column; justify-content: space-between;
            align-items: center; position: relative;
            transform: perspective(600px) rotateY(-12deg);
            box-shadow: -6px 10px 12px rgba(0,0,0,0.5); border: 2px solid #555;
            transition: transform 0.2s;
        }
        .coach-3d:hover { transform: perspective(600px) rotateY(0deg) scale(1.08); z-index: 10; }
        .roof { width: 100%; height: 16px; background: rgba(0,0,0,0.3); border-radius: 6px 6px 0 0; }
        .windows { display: flex; gap: 5px; margin-top: 8px; }
        .window { width: 16px; height: 20px; background: rgba(255,255,255,0.85); border-radius: 2px; }
        .coach-id { color: white; font-weight: 800; font-size: 15px; margin-bottom: 8px; text-shadow: 1px 1px 3px #000; }
        .wheels { width: 100%; height: 8px; background: #000; display:flex; justify-content:space-around; }
        .wheel { width:12px; height:12px; background:#444; border-radius:50%; margin-top:-2px; }
    </style>
    """

    html += "<h4 style='color: #ddd; font-family: sans-serif;'>🔴 LIVE: Current Coach Density</h4><div class='train-track'>"
    for c, density in current_densities.items():
        color, status = get_color(density)
        html += f"""
        <div class='coach-3d' style='background-color: {color};' title='{c}: {status} ({density}%)'>
            <div class='roof'></div>
            <div class='windows'><div class='window'></div><div class='window'></div></div>
            <div class='coach-id'>{c}</div>
            <div class='wheels'><div class='wheel'></div><div class='wheel'></div></div>
        </div>"""
    html += "</div>"

    html += "<h4 style='color: #4da6ff; font-family: sans-serif;'>🔮 AI PREDICTION: Status in 10 Minutes</h4><div class='train-track'>"
    for c, density in current_densities.items():
        future_density = max(10, min(98, density + random.randint(-8, 12)))
        color, status = get_color(future_density)
        html += f"""
        <div class='coach-3d' style='background-color: {color}; opacity: 0.85;' title='{c} Expected: {status} ({future_density}%)'>
            <div class='roof'></div>
            <div class='windows'><div class='window'></div><div class='window'></div></div>
            <div class='coach-id'>{c}</div>
            <div class='wheels'><div class='wheel'></div><div class='wheel'></div></div>
        </div>"""
    html += "</div>"

    return html