from datetime import datetime
import random

def get_womens_helpline():
    return "📞 Railway Police: 1512 | 🚓 Women Helpline: 1091"

def trigger_sos_alert(username, current_location):
    """Generates a secure live-tracking link and emergency payload"""
    incident_id = random.randint(10000, 99999)
    tracking_link = f"https://pulse-safe.com/track/{username.replace(' ', '')}-{incident_id}"
    
    emergency_payload = {
        "user": username,
        "last_seen": current_location,
        "time": datetime.now().strftime("%H:%M:%S"),
        "status": "🔴 HIGH ALERT - SOS TRIGGERED",
        "share_link": tracking_link
    }
    return emergency_payload
