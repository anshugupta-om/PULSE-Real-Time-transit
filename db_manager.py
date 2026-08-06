# db_manager.py - Centralized Master CSV Audit Logging Engine

import os
import pandas as pd
from datetime import datetime

MASTER_AUDIT_CSV = 'master_system_audit_logs.csv'

def init_master_csv():
    """Ensures Master Audit CSV structure exists"""
    if not os.path.exists(MASTER_AUDIT_CSV):
        df = pd.DataFrame(columns=[
            "Timestamp", 
            "Username", 
            "Activity Category", 
            "Source / Location", 
            "Destination / Action", 
            "Intent / Purpose / Query", 
            "System Status Mode"
        ])
        df.to_csv(MASTER_AUDIT_CSV, index=False)

def append_audit_log(username, category, source_loc, dest_action, intent_details, mode="ONLINE"):
    """Appends detailed activity logs for Admin Master CSV Sheet"""
    init_master_csv()
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {
            "Timestamp": timestamp,
            "Username": username,
            "Activity Category": category,
            "Source / Location": source_loc if source_loc else "N/A",
            "Destination / Action": dest_action if dest_action else "N/A",
            "Intent / Purpose / Query": intent_details if intent_details else "General Session",
            "System Status Mode": mode
        }
        
        df = pd.read_csv(MASTER_AUDIT_CSV)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(MASTER_AUDIT_CSV, index=False)
    except Exception as e:
        print(f"[CHAT LOG] User: {username} | Action: {dest_action} | Details: {intent_details} | Mode: {mode}")

def log_login_event(username, role="user"):
    append_audit_log(username, "USER_LOGIN", "Enterprise Portal", "Session Granted", f"User logged in successfully as {role}", "AUTHENTICATED")

def log_journey_event(username, line, source, dest):
    append_audit_log(username, "JOURNEY_SEARCH", f"{line} ({source})", dest, f"Commuter route search from {source} to {dest}", "LIVE_TRACKING")

def log_chat_message(username, action_type, message, mode):
    append_audit_log(username, "CHATBOT_INTERACTION", "Pulse Buddy AI", action_type, message, mode)

# Dummy SQL functions to avoid import errors from legacy modules
def log_journey_sql(journey_id, username, line, source, dest, status):
    log_journey_event(username, line, source, dest)

def get_admin_dataframe():
    init_master_csv()
    return pd.read_csv(MASTER_AUDIT_CSV)

def clear_all_data():
    if os.path.exists(MASTER_AUDIT_CSV):
        os.remove(MASTER_AUDIT_CSV)
    init_master_csv()

def get_next_journey_id():
    import random
    return random.randint(10000, 99999)