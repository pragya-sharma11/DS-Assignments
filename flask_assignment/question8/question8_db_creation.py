# import sqlite3 module 
import sqlite3
# connect the database "database.db"
conn = sqlite3.connect("database.db")
print("opened the database successfully")
# execute create table query to create a table for LIVE_USERS having columns username, password
conn.execute("CREATE TABLE LIVE_USERS (username TEXT primary_key, password TEXT)")
print("Table created successfully")
# close the connection
conn.close()