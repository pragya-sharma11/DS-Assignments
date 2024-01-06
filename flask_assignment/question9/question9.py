# 9. Create a RESTful API using Flask to perform CRUD operations on resources like books or movies.

# import everything from flask module
from flask import * 
# import sqlite3 for database connection
import sqlite3

# create Flask application object in current module
app = Flask(__name__)

# create a route for home page
@app.route('/')
def show_details():
    # connect with database
    conn = sqlite3.connect('database.db')
    # get a row_factory to inspect the rquery result and prepare a callable 
    conn.row_factory = sqlite3.Row
    # create Cursor object using the cursor() method of the Connection object/class
    cur = conn.cursor()
    # select all records from books table
    cur.execute("SELECT * FROM BOOKS")
    # fetch all rows
    rows = cur.fetchall()
    # render the homepage template.
    return render_template('quest9_template_homepage.html', rows = rows)

# add route to insert a new record
@app.route('/add_rec')
def add_record():
    # render the template to insert record
    return render_template('quest9_template_insert.html')

# add a route to insert 
@app.route('/insertion', methods = ['POST'])
def insertions():
    # get book_id from form
    book_id = request.form['book_id']
    # get author from form
    author = request.form['author']
    # get book from form
    book_name = request.form['book']
    # connect with database
    with sqlite3.connect('database.db') as conn:
        # get a row_factory to inspect the rquery result and prepare a callable 
        conn.row_factory = sqlite3.Row
        # create Cursor object using the cursor() method of the Connection object/class
        cur = conn.cursor()
        # get all records where bookid matches with form book_id
        row = cur.execute("SELECT * FROM BOOKS where book_id = ?", (book_id,))
        # fetch one row
        row = row.fetchone()
        # if row exists and book_id matches with row's book_id
        if row and book_id == row['book_id']:
            # return a page with add book link as this book is already existed
            return 'Book Existed with this book id, please try with another book id <a href="/add_rec">Add Book</a>'
        # if row doesn't existed
        else:
            # create a try block
            try:
                # # create Cursor object using the cursor() method of the Connection object/class 
                cur = conn.cursor()
                # insert a new record in Books table 
                cur.execute('INSERT into BOOKS VALUES(?,?,?)',(book_id, author,book_name))
                # get variable with message
                msg = 'Insertion is successful'
            # create an except block
            except:
                # rollback operation if exception occurs
                conn.rollback()
                print('error')
                # get variable with message
                msg = 'Error in insertion operation.'
            # create a finally block
            finally : 
                # redirect to main page
                return redirect('/')
# create a route for update operation
@app.route('/<BOOK_ID>/update', methods = ['POST', 'GET'])
def update(BOOK_ID):
    # connect with database
    with sqlite3.connect('database.db') as conn:
        # get a row_factory to inspect the rquery result and prepare a callable 
        conn.row_factory = sqlite3.Row
        # create Cursor object using the cursor() method of the Connection object/class
        cur = conn.cursor()
        # select row from Books table where bookid matches with form's book_id
        row = cur.execute("SELECT * FROM BOOKS where book_id = ?", (BOOK_ID,))
        # fetch one row
        row = row.fetchone()
        # if row exists and book_id matches
        if row and BOOK_ID == row['book_id']:
            # render template and pass row data in the template
            return render_template('quest9_template_updation.html', row = row)
        # redirect to home page
        return redirect('/')
# add a route for updating records
@app.route('/updation', methods = ['POST'])
def update_book_record():
    # get book_id from form
    book_id = request.form['book_id']
    # get author from form
    author = request.form['author']
    # get book_name from form
    book_name = request.form['book']
    # connect with database
    with sqlite3.connect('database.db') as conn:
        # # get a row_factory to inspect the rquery result and prepare a callable 
        conn.row_factory = sqlite3.Row
        # create Cursor object using the cursor() method of the Connection object/class
        cur = conn.cursor()
        # create a try block
        try: 
            # # create Cursor object using the cursor() method of the Connection object/class
            cur = conn.cursor()
            # update records where book_id matches with row's book_id
            cur.execute("UPDATE BOOKS set AUTHOR = ?, BOOK_NAME = ? where BOOK_ID = ?", (author, book_name,book_id))
            # initialize a variable for successful updation
            msg = 'Updation is successful'
        # create an except block
        except:
            # rollback the operation if there is an exception 
            conn.rollback()
            # initialize a variable for unsuccessful updation
            msg = 'Error in updation operation.'
        # create finally block
        finally : 
            # redirect to home page
            return redirect('/')
        


# add route for deletion of record
@app.route('/<BOOK_ID>/delete', methods = ['POST', 'GET'])
def delete(BOOK_ID):
    # connect with database
    with sqlite3.connect('database.db') as conn:
        # get a row_factory to inspect the rquery result and prepare a callable 
        conn.row_factory = sqlite3.Row
        # create Cursor object using the cursor() method of the Connection object/class
        cur = conn.cursor()
        # create a try block 
        try:
            # delete the record whose book_id matches with form's book_id
            cur.execute("DELETE FROM BOOKS where book_id = ?", (BOOK_ID,))
            # commit orperation
            conn.commit()
            # initialize a variable for unsuccessful deletion
            msg = 'Error in deletion operation'
        # create an except block
        except sqlite3.Error as error:
            # rollback the operation
            conn.rollback()
            print(error)
            # initialize a variable for unsuccessful deletion
            msg = "Book_id doesn't exist"
        # create a finally block
        finally : 
            # redirect to home page
            return redirect('/')

                # return msg + " <a href = '/'>Go back to home</a>"
# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)