import sqlite3
import pandas as pd

conn = sqlite3.connect('carboncut.db')
try:
    df = pd.read_sql_query("SELECT * FROM impact_results", conn)
    print("Database Contents:")
    print(df)
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()