# 9. Create a RESTful API using Flask to perform CRUD operations on resources like books or movies.

from flask import * 
import sqlite3
app = Flask(__name__)

@app.route('/')
def show_details():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM BOOKS")
    rows = cur.fetchall()
    return render_template('quest9_template_homepage.html', rows = rows)

@app.route('/add_rec')
def add_record():
    return render_template('quest9_template_insert.html')

@app.route('/insertion', methods = ['POST'])
def insertions():
    book_id = request.form['book_id']
    author = request.form['author']
    book_name = request.form['book']
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        row = cur.execute("SELECT * FROM BOOKS where book_id = ?", (book_id,))
        row = row.fetchone()
        if row and book_id == row['book_id']:
            return 'Book Existed with this book id, please try with another book id <a href="/add_rec">Add Book</a>'
        else:
            try: 
                cur = conn.cursor()
                cur.execute('INSERT into BOOKS VALUES(?,?,?)',(book_id, author,book_name))
                msg = 'Insertion is successful'
            except:
                conn.rollback()
                print('error')
                msg = 'Error in insertion operation.'
            finally : 
                return redirect('/')

@app.route('/<BOOK_ID>/update', methods = ['POST', 'GET'])
def update(BOOK_ID):
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        row = cur.execute("SELECT * FROM BOOKS where book_id = ?", (BOOK_ID,))
        row = row.fetchone()
        if row and BOOK_ID == row['book_id']:
            return render_template('quest9_template_updation.html', row = row)
        return redirect('/')

@app.route('/updation', methods = ['POST'])
def update_book_record():
    book_id = request.form['book_id']
    author = request.form['author']
    book_name = request.form['book']
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        try: 
            cur = conn.cursor()
            cur.execute("UPDATE BOOKS set AUTHOR = ?, BOOK_NAME = ? where BOOK_ID = ?", (author, book_name,book_id))
            msg = 'Updation is successful'
        except:
            conn.rollback()
            msg = 'Error in updation operation.'
        finally : 
            return redirect('/')
        



@app.route('/<BOOK_ID>/delete', methods = ['POST', 'GET'])
def delete(BOOK_ID):
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM BOOKS where book_id = ?", (BOOK_ID,))
            conn.commit()
            msg = 'Error in deletion operation'
        except sqlite3.Error as error:
            conn.rollback()
            print(error)
            msg = "Book_id doesn't exist"
        finally : 
            return redirect('/')

                # return msg + " <a href = '/'>Go back to home</a>"
# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)