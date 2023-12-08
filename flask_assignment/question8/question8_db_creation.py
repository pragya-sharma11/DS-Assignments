import sqlite3

conn = sqlite3.connect("database.db")
print("opened the database successfully")
conn.execute("CREATE TABLE LIVE_USERS (username TEXT primary_key, password TEXT)")
print("Table created successfully")
conn.close()