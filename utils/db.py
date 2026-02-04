import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('appaty.db', check_same_thread=False)
    c = conn.cursor()
    # Create Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, 
                  password TEXT, 
                  is_premium INTEGER DEFAULT 0)''')
    
    # Create History Table (Required by app.py)
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  calc_name TEXT, 
                  result TEXT,
                  timestamp TEXT,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
                  
    conn.commit()
    conn.close()

def add_user(username, password):
    try:
        conn = sqlite3.connect('appaty.db', check_same_thread=False)
        c = conn.cursor()
        # Password is expected to be already hashed by auth.py
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username.lower().strip(), password))
        conn.commit()
        conn.close()
        return True, "User registered successfully!"
    except sqlite3.IntegrityError:
        return False, "This username is already taken!"

def get_user(username):
    conn = sqlite3.connect('appaty.db', check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM users WHERE username = ?", conn, params=(username.lower().strip(),))
    conn.close()
    return df

# --- Legacy Support for app.py ---

def add_history_item(user_id, calc_name, result):
    """Save calculation to history (Required by app.py)."""
    conn = sqlite3.connect('appaty.db', check_same_thread=False)
    c = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('INSERT INTO history (user_id, calc_name, result, timestamp) VALUES (?, ?, ?, ?)',
              (user_id, calc_name, str(result), timestamp))
    conn.commit()
    conn.close()

def toggle_premium(user_id):
    """Toggle premium status for a user."""
    conn = sqlite3.connect('appaty.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute('SELECT is_premium FROM users WHERE id = ?', (user_id,))
    res = c.fetchone()
    new_status = 0
    if res:
        current = res[0]
        new_status = 0 if current else 1
        c.execute('UPDATE users SET is_premium = ? WHERE id = ?', (new_status, user_id))
        conn.commit()
    
    conn.close()
    return bool(new_status)
