import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Simulated Mumbai Data [cite: 10, 81]
# station_id: 1: Churchgate, 2: Dadar, 3: Andheri, 4: Borivali, 5: Virar
data = {
    'station_id': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
    'hour': [9, 10, 18, 19, 9, 15, 10, 18, 19, 21], 
    'is_peak': [1, 1, 1, 1, 1, 0, 1, 1, 1, 0], # [cite: 39, 84]
    'is_monsoon': [0, 0, 1, 1, 0, 0, 1, 1, 0, 0], # [cite: 40, 166]
    'delay': [2, 5, 15, 20, 2, 1, 6, 18, 25, 4] 
}

df = pd.DataFrame(data)
X = df.drop('delay', axis=1)
y = df['delay']

model = RandomForestRegressor(n_estimators=100, random_state=42) # [cite: 92, 118]
model.fit(X, y)

joblib.dump(model, 'mumbai_model.pkl') # [cite: 181]
print("Model trained: mumbai_model.pkl created!")