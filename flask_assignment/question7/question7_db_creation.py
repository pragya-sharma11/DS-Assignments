import sqlite3

conn = sqlite3.connect("database.db")
print("opened the database successfully")
conn.execute("CREATE TABLE EMPLOYEE (e_id TEXT primary_key, name TEXT, city TEXT, country TEXT)")
print("Table created successfully")
conn.close()