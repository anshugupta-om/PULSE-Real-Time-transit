def get_station_hazard(station_name):
    """Returns historical accident risks for specific Mumbai stations"""
    hazards = {
        "Dadar": "⚠️ High Stampede Risk on Platform 3/4. Use Foot Overbridge carefully.",
        "Kurla": "⚠️ Dangerous Platform Gap. Mind your step while boarding.",
        "Borivali": "⚠️ Heavy door-blocking reported. Do not stand at the edge.",
        "Andheri East": "⚠️ Slippery platforms due to monsoon. Walk slowly.",
        "CSMT": "✅ Station operations normal and safe."
    }
    # Agar station list me nahi hai, toh default message:
    return hazards.get(station_name, "✅ Normal crowd movement.")

def check_deboarding_risk(current_eta):
    """Prevents jumping off moving trains by giving an alert 3 mins before arrival"""
    if current_eta <= 3:
        return "🛑 ALIGHTING ALERT: Train arriving soon. Do NOT jump before the train stops!"
    return None