import pandas as pd
import joblib

def predict_local_train(station, line, hour, is_monsoon):
    # Mumbai Specific Factors [cite: 165]
    base_delay = 2 # Normal delay
    
    # Peak Hour Logic (8-11 AM & 5-8 PM) [cite: 84, 157]
    if (8 <= hour <= 11) or (17 <= hour <= 20):
        base_delay += 10
    
    # Monsoon Impact (Rain delays 15-30%) [cite: 40, 166]
    if is_monsoon:
        base_delay += 15
        
    # Crowd Density Score [cite: 155, 158]
    crowd_score = "High (85%)" if (8 <= hour <= 11) else "Low (30%)"
    
    return base_delay, crowd_score