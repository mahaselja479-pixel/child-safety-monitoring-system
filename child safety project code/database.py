import sqlite3
from datetime import datetime  # To get current date and time

# Connect to database
conn = sqlite3.connect("emotion.db")
cursor = conn.cursor()

# Step 1: Create table with timestamp column
cursor.execute("""
CREATE TABLE IF NOT EXISTS emotions (
    emotion TEXT,
    alert TEXT,
    timestamp TEXT
)
""")

# Step 2: Insert data with current time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cursor.execute("INSERT INTO emotions VALUES (?, ?, ?)", ('Fear', 'Alert Sent', current_time))

# Step 3: Fetch and display data
cursor.execute("SELECT * FROM emotions")
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close connection
conn.commit()
conn.close()