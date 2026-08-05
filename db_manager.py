import sqlite3
import pandas as pd
from datetime import datetime

# 1. Database aur Table Create karna (Naya Structure 'journey_id' ke sath)
def init_db():
    conn = sqlite3.connect('pulse_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transit_logs
                 (journey_id INTEGER, timestamp TEXT, username TEXT, line TEXT, source TEXT, destination TEXT, status TEXT)''')
    conn.commit()
    conn.close()

# 2. Naya Serial Number (Journey ID) banana
def get_next_journey_id():
    conn = sqlite3.connect('pulse_database.db')
    c = conn.cursor()
    c.execute("SELECT MAX(journey_id) FROM transit_logs")
    result = c.fetchone()[0]
    conn.close()
    return 1 if result is None else result + 1

# 3. Data Insert karna (Ab isme journey_id bhi jayega)
def log_journey_sql(journey_id, username, line, source, destination, status):
    conn = sqlite3.connect('pulse_database.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO transit_logs VALUES (?, ?, ?, ?, ?, ?, ?)",
              (journey_id, timestamp, username, line, source, destination, status))
    conn.commit()
    conn.close()

# 4. Admin Panel ke liye Data wapas nikalna (Excel jaisa clean format)
def get_admin_dataframe():
    conn = sqlite3.connect('pulse_database.db')
    # Order by journey_id (Sr No) taaki ek journey ka data ek sath dikhe
    df = pd.read_sql_query("SELECT * FROM transit_logs ORDER BY journey_id DESC, timestamp ASC", conn)
    conn.close()
    
    # Dataframe ke columns ka naam professional kar diya
    df.columns = ["Sr No", "Time", "User", "Line", "From", "To", "Status"]
    return df

# 5. Database clear karne ke liye
def clear_all_data():
    conn = sqlite3.connect('pulse_database.db')
    c = conn.cursor()
    c.execute("DELETE FROM transit_logs")
    conn.commit()
    conn.close()

# Start hote hi DB initialize kar do
init_db()