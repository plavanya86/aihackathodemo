import sqlite3

DB_PATH="C:/Users/pamarthi.padmavathi/git/aihackathodemo/ai_rangers.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM tasks")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()