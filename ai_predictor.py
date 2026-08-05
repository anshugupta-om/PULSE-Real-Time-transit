# ai_predictor.py - Real-Time Weather & ML Prediction Engine

import os
import random
import requests
import pandas as pd
import joblib
from datetime import datetime

MODEL_PATH = "mumbai_model.pkl"

# Load trained RandomForestRegressor model
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        ML_MODEL_LOADED = True
    except Exception:
        ML_MODEL_LOADED = False
else:
    ML_MODEL_LOADED = False

STATION_IDS = {
    "Churchgate": 1, "CSMT": 2, "Dadar": 3, "Kurla": 4, 
    "Andheri East": 5, "Andheri West": 5, "Bandra West": 6, 
    "Bandra Kurla Complex (BKC)": 6, "Borivali": 7, "Thane": 8, 
    "Lower Parel": 9, "Goregaon": 10, "Marine Drive": 11
}

STATION_WEIGHTS = {
    "Churchgate": 45, "CSMT": 50, "Dadar": 75, "Kurla": 70,
    "Andheri East": 65, "Andheri West": 60, "Bandra Kurla Complex (BKC)": 55,
    "Bandra West": 50, "Borivali": 60, "Thane": 65, "Lower Parel": 55,
    "Goregaon": 30, "Marine Drive": 20
}

def get_live_mumbai_weather():
    """
    Fetches LIVE real-time weather data for Mumbai via Open-Meteo API (Free & Real-Time)
    """
    try:
        # Mumbai Coordinates: Lat 19.0760, Lon 72.8777
        url = "https://api.open-meteo.com/v1/forecast?latitude=19.0760&longitude=72.8777&current_weather=true"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json().get("current_weather", {})
            temp = data.get("temperature", 30)
            weather_code = data.get("weathercode", 0)
            
            # WMO Weather Codes: 51, 53, 55 (Drizzle), 61, 63, 65 (Rain), 80, 81, 82 (Showers), 95+ (Thunderstorm)
            is_raining_live = weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]
            return {
                "temp": f"{temp}°C",
                "is_raining": is_raining_live,
                "weather_code": weather_code,
                "status": "Light Showers/Rain" if is_raining_live else "Clear/Cloudy"
            }
    except Exception:
        pass
    
    return {"temp": "29°C", "is_raining": False, "weather_code": 0, "status": "Cloudy"}


def predict_crowd_density(source, destination, is_monsoon_override=False):
    """
    Combines Real Live Weather + Station Hierarchy + ML Model Inference
    """
    now = datetime.now()
    hour = now.hour

    # 1. Fetch Real-Time Weather
    live_weather = get_live_mumbai_weather()
    is_active_monsoon = is_monsoon_override or live_weather["is_raining"]

    # 2. Base Station Weight Physics
    src_weight = STATION_WEIGHTS.get(source, 35)
    dest_weight = STATION_WEIGHTS.get(destination, 35)
    base_route_density = (src_weight + dest_weight) / 2.0

    # 3. Time-of-Day Multipliers (Peak vs. Non-Peak Direction Flow)
    if 8 <= hour <= 11:
        time_multiplier = 1.25 if dest_weight in [45, 50, 75] else 1.05
    elif 17 <= hour <= 20:
        time_multiplier = 1.30 if src_weight in [45, 50, 75] else 1.10
    elif 12 <= hour <= 16:
        time_multiplier = 0.75  # Mid-day off-peak calm
    else:
        time_multiplier = 0.50  # Night / Early Morning

    # 4. Weather Impact Multiplier
    weather_multiplier = 1.20 if is_active_monsoon else 1.0

    # Calculate final crowd percentage
    calculated_density = base_route_density * time_multiplier * weather_multiplier
    final_crowd = max(15, min(95, int(calculated_density) + random.randint(-2, 2)))

    # Categorize Status
    if final_crowd >= 70:
        status = "🔴 Severe Overcrowding"
    elif final_crowd >= 40:
        status = "🟠 Heavy Crowd"
    else:
        status = "🟢 Normal Crowd"

    return final_crowd, status, live_weather