import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = 'carboncut.db'

def init_db():
    """Initializes the database with the required 'rating' column to prevent OperationalErrors."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                hardware TEXT,
                epochs INTEGER,
                kg_saved REAL,
                tree_days REAL,
                phone_charges INTEGER,
                rating TEXT
            )
        ''')
        conn.commit()

def seed_hardware():
    """Kept for dashboard compatibility."""
    pass

def save_full_audit(hw_name, old_code, green_code, epochs, kg_saved, tree_days, charges):
    """Saves the audit and assigns a performance badge based on savings."""
    if kg_saved > 0.0001:
        rating = "🍃 High Impact"
    elif kg_saved > 0:
        rating = "🌱 Efficient"
    else:
        rating = "⚠️ Low Load"

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%b %d, %H:%M")
        cursor.execute('''
            INSERT INTO audits (timestamp, hardware, epochs, kg_saved, tree_days, phone_charges, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, hw_name, epochs, kg_saved, tree_days, charges, rating))
        conn.commit()

def get_recent_history():
    """Fetches history for the Streamlit UI history page."""
    with sqlite3.connect(DB_NAME) as conn:
        query = '''
            SELECT timestamp as "Time", 
                   hardware as "Device", 
                   rating as "Performance",
                   kg_saved as "CO2 Saved (kg)", 
                   tree_days as "Tree Restoration (Days)" 
            FROM audits 
            ORDER BY id DESC LIMIT 15
        '''
        return pd.read_sql_query(query, conn)

def clear_all_history():
    """Utility to wipe the database for fresh demonstrations."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DELETE FROM audits')
        conn.commit()

__all__ = ["init_db", "seed_hardware", "save_full_audit", "get_recent_history", "clear_all_history"]