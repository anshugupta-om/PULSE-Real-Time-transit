import random
from datetime import datetime

def predict_crowd_density(source, destination, is_monsoon):
    hour = datetime.now().hour
    
    # Base crowd calculation algorithm
    base_crowd = 40 # Minimum 40% crowd in Mumbai always!
    
    # Peak hour impact
    if 8 <= hour <= 11 or 17 <= hour <= 20:
        base_crowd += 35 
        
    # Weather impact
    if is_monsoon:
        base_crowd += 15 
        
    # Route specific logic (e.g., Dadar is always crowded)
    if "Dadar" in source or "Dadar" in destination:
        base_crowd += 10
        
    # Add slight random fluctuation for realism
    final_crowd = min(100, base_crowd + random.randint(-5, 5))
    
    # Categorize the result
    if final_crowd >= 85:
        status = "🔴 Severe Overcrowding"
    elif final_crowd >= 65:
        status = "🟠 Heavy Crowd"
    else:
        status = "🟢 Normal Crowd"
        
    return final_crowd, status

# Test code (Jab is file ko direct run karogi)
if __name__ == "__main__":
    density, status = predict_crowd_density("Andheri", "Dadar", True)
    print(f"Prediction: {density}% - {status}")