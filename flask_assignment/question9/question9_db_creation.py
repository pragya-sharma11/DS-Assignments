import sqlite3

conn = sqlite3.connect("database.db")
print("opened the database successfully")
conn.execute("CREATE TABLE BOOKS (BOOK_ID TEXT primary key, AUTHOR TEXT , BOOK_NAME TEXT)")
print("Table created successfully")
conn.close()