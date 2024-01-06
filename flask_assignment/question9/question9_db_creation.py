# import sqlite3 module 
import sqlite3
# connect the database "database.db"
conn = sqlite3.connect("database.db")
print("opened the database successfully")
# execute create table query to create a table for Books having columns booki_id, author, book_name
conn.execute("CREATE TABLE BOOKS (BOOK_ID TEXT primary key, AUTHOR TEXT , BOOK_NAME TEXT)")
print("Table created successfully")
# close the connection
conn.close()