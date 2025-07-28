import sqlite3
import pandas as pd

try:
    # Connect to data.db
    conn = sqlite3.connect("data.db")
    
    # Query the framingham table
    df = pd.read_sql_query("SELECT * FROM framingham", conn)
    
    # Display the data
    print("Framingham Table Contents:")
    print(df)
    
    # Optionally, save to CSV
    df.to_csv("framingham_data.csv", index=False)
    print("Data saved to framingham_data.csv")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()