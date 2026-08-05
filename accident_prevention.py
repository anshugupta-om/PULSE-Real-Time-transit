def check_accident_risk(crowd_density, station, is_monsoon):
    """
    Evaluates the risk of stampedes or boarding accidents
    based on live crowd density and environmental factors.
    """
    # Base risk tied directly to how crowded the station is
    risk_score = crowd_density * 0.60
    
    # Historical high-incident stations in Mumbai
    high_risk_stations = ["Dadar", "Kurla", "Thane", "Andheri", "Borivali"]
    if any(hub in station for hub in high_risk_stations):
        risk_score += 20
        
    # Weather conditions severely impact platform safety (slippery edges)
    if is_monsoon:
        risk_score += 15
        
    # Cap the risk score at 100%
    risk_score = min(100, risk_score)
        
    # Determine alert level and required actions
    if risk_score >= 85:
        level = "CRITICAL RISK"
        color = "🔴"
        action = "Deploy RPF immediately. Halt escalator entry and restrict footbridge access."
    elif risk_score >= 60:
        level = "MODERATE RISK"
        color = "🟠"
        action = "Issue continuous PA announcements. Monitor platform clearance."
    else:
        level = "LOW RISK"
        color = "🟢"
        action = "Standard operating procedures. Normal platform conditions."
        
    return {
        "risk_percentage": round(risk_score, 1),
        "alert_level": level,
        "indicator": color,
        "recommended_action": action
    }

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

# Test code
if __name__ == "__main__":
    # Testing the accident risk logic
    risk_assessment = check_accident_risk(88, "Kurla", True)
    print(f"{risk_assessment['indicator']} {risk_assessment['alert_level']} ({risk_assessment['risk_percentage']}%)")
    print(f"Action: {risk_assessment['recommended_action']}\n")
    
    # Testing the new station hazard logic
    print(f"Hazard at Kurla: {get_station_hazard('Kurla')}")
    print(f"Hazard at Vashi: {get_station_hazard('Vashi')}\n")
    
    # Testing the new deboarding risk logic
    print(f"ETA 5 mins: {check_deboarding_risk(5)}")
    print(f"ETA 2 mins: {check_deboarding_risk(2)}")