# import sqlite3 module 
import sqlite3

# connect the database "database.db"
conn = sqlite3.connect("database.db")
print("opened the database successfully")
# execute create table query to create a table for employee having columns e_id, name, city, country
conn.execute("CREATE TABLE EMPLOYEE (e_id TEXT primary_key, name TEXT, city TEXT, country TEXT)")
print("Table created successfully")
# close the connection
conn.close()