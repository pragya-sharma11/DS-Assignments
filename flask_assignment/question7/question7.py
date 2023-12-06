# 7. Integrate a SQLite database with Flask to perform CRUD operations on a list of items.

from flask import * 
import sqlite3
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('quest7_template_home_page.html')
@app.route('/add_employee')
def add_employee_details():
    return render_template('quest7_template_insertion_operation.html')

@app.route('/addrec', methods = ['POST'])
def addrec():
    emp_id = request.form['emp_id']
    name = request.form['name']
    city = request.form['city']
    country = request.form['country']
    with sqlite3.connect('database.db') as conn:
        print("Database is opened again")
        try: 
            cur = conn.cursor()
            cur.execute('INSERT into EMPLOYEE VALUES(?,?,?,?)',(emp_id, name, city, country))
            print(emp_id, name, city, country)
            msg = 'Insertion is successful'
        except:
            conn.rollback()
            msg = 'Error in insertion operation.'
        finally : 
            return render_template('quest7_template_operation_result.html', msg = msg)
            
@app.route('/display_employee')
def show_details():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM EMPLOYEE")
    rows = cur.fetchall()
    return render_template('quest7_template_display_operation.html', rows = rows)

@app.route('/update_employee')
def update_details():
    return render_template('quest7_template_update_operation.html')

@app.route('/update', methods = ['POST'])
def update():
    emp_id = request.form['emp_id']
    city = request.form['city']
    country = request.form['country']
    with sqlite3.connect('database.db') as conn:
        print("Database is opened again")
        try: 
            cur = conn.cursor()
            cur.execute('UPDATE EMPLOYEE SET city = ?, country=? where e_id = ?',(city, country, emp_id))
            print(emp_id, city, country)
            msg = 'Updation is successful'
        except:
            conn.rollback()
            msg = 'Error in updation operation.'
        finally : 
            return render_template('quest7_template_operation_result.html', msg = msg)

@app.route('/delete_employee')
def delete_details():
    return render_template('quest7_template_delete_operation.html')

@app.route('/delete', methods = ['POST'])
def delete_employee():
    emp_id = request.form['emp_id']
    print(emp_id)
    with sqlite3.connect('database.db') as conn:
        print("Database is opened again")
        try: 
            cur = conn.cursor()
            cur.execute('DELETE FROM EMPLOYEE WHERE e_id = ?', (emp_id,))
            conn.commit()
            print(emp_id)
            msg = 'Deletion is successful'
        except sqlite3.Error as error:
            conn.rollback()
            print(error)
            msg = 'Error in deletion operation.'
        finally : 
            return render_template('quest7_template_operation_result.html', msg = msg)


# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)