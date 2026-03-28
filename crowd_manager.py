import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

def get_live_waiting_count(source_station):
    """Sirf un users ko ginta hai jo 'Right Now' (last 30s) active hain"""
    try:
        conn = sqlite3.connect('pulse_database.db')
        time_threshold = (datetime.now() - timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S")
        
        query = f"""
            SELECT COUNT(DISTINCT username) 
            FROM transit_logs 
            WHERE source = '{source_station}' 
            AND timestamp >= '{time_threshold}'
        """
        count = pd.read_sql_query(query, conn).iloc[0, 0]
        conn.close()
        return count
    except:
        return 0

def get_admin_recommendation(current_crowd):
    # Agar 5 se zyada users (demo ke liye) ek saath hain toh alert
    threshold = 5 
    if current_crowd >= threshold:
        return {
            "status": "🔴 OVERCROWDED",
            "message": f"Alert: Platform is crowded ({current_crowd} active users). Consider alternatives.",
            "alternatives": [
                {"mode": "🛺 Auto", "price": "₹60"},
                {"mode": "🚕 Taxi", "price": "₹150"}
            ]
        }
    return {"status": "🟢 NORMAL", "message": "Crowd is manageable.", "alternatives": []}