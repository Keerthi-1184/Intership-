import sqlite3
import pandas as pd

try:
    # Connect to data.db
    conn = sqlite3.connect("data.db")
    
    # List all tables
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in data.db:", [table[0] for table in tables])
    
    # Query each table and display data
    for table in tables:
        table_name = table[0]
        print(f"\nData in table '{table_name}':")
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        print(df)
    
    # Close connection
    conn.close()
except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")