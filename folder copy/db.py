import sqlite3

conn = sqlite3.connect('score.db')

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     score INTEGER
)
""")
conn.commit()
