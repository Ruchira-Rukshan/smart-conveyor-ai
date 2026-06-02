import sqlite3
import datetime
import pandas as pd

DB_NAME = 'garbage_stats.db'

def init_db():
    """Initializes the database and creates the necessary tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Table to store individual item detections
    c.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            class_name TEXT,
            track_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def log_detection(class_name, track_id):
    """
    Logs a new detection.
    To avoid counting the same object multiple times, we also store the track_id.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Check if this track_id has already been logged today for this class
    # (Assuming track IDs might reset, we only care about uniqueness within the current session/day, 
    # but for simplicity, we check if it exists at all to avoid duplicates).
    c.execute('''
        SELECT COUNT(*) FROM detections 
        WHERE class_name = ? AND track_id = ?
    ''', (class_name, track_id))
    
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO detections (timestamp, class_name, track_id)
            VALUES (?, ?, ?)
        ''', (datetime.datetime.now(), class_name, track_id))
        conn.commit()
        logged = True
    else:
        logged = False
        
    conn.close()
    return logged

def get_today_stats():
    """Returns a pandas dataframe with the count of each class detected today."""
    conn = sqlite3.connect(DB_NAME)
    
    # Get today's date in YYYY-MM-DD format
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    query = f"""
        SELECT class_name, COUNT(*) as count 
        FROM detections 
        WHERE date(timestamp) = '{today}'
        GROUP BY class_name
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_all_time_stats():
    """Returns a pandas dataframe with all-time detection counts."""
    conn = sqlite3.connect(DB_NAME)
    
    query = """
        SELECT class_name, COUNT(*) as count 
        FROM detections 
        GROUP BY class_name
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
