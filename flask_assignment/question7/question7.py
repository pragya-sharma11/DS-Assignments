# 7. Integrate a SQLite database with Flask to perform CRUD operations on a list of items.

# import everything from flask module
from flask import * 
# import sqlite3 for database connection
import sqlite3

# create Flask application object in current module
app = Flask(__name__)

# create a route for home page
@app.route('/')
def home():
    # render the home page template
    return render_template('quest7_template_home_page.html')
# create a route for adding an employee details
@app.route('/add_employee')
def add_employee_details():
    # render template to insert employee data
    return render_template('quest7_template_insertion_operation.html')

# create a route to add a record
@app.route('/addrec', methods = ['POST'])
def addrec():
    # get emp_id from form
    emp_id = request.form['emp_id']
    # get name from form
    name = request.form['name']
    # get city from form
    city = request.form['city']
    # get country from form
    country = request.form['country']
    # connect with database
    with sqlite3.connect('database.db') as conn:
        print("Database is opened again")
        # start try block
        try: 
            # create Cursor object using the cursor() method of the Connection object/class
            cur = conn.cursor()
            # insert all the details into database which we get from form
            cur.execute('INSERT into EMPLOYEE VALUES(?,?,?,?)',(emp_id, name, city, country))
            print(emp_id, name, city, country)
            # initialize a message for successful insertion
            msg = 'Insertion is successful'
        # create a except block
        except:
            # if there is an exception we can simply rollback
            conn.rollback()
            # initialize a message for unsuccessful insertion
            msg = 'Error in insertion operation.'
        # create a finally block
        finally : 
            # render a template for result of operation page
            return render_template('quest7_template_operation_result.html', msg = msg)
            
# create a route for diplaying the employee details
@app.route('/display_employee')
def show_details():
    # connect with the database 
    conn = sqlite3.connect('database.db')
    # fetch rows
    conn.row_factory = sqlite3.Row
    # get the cursor
    cur = conn.cursor()
    # select all the data from employee table
    cur.execute("SELECT * FROM EMPLOYEE")
    # fetch all the records
    rows = cur.fetchall()
    # render the template to display the data and pass all the rows
    return render_template('quest7_template_display_operation.html', rows = rows)

# add a route to get form for updating details of employee
@app.route('/update_employee')
def update_details():
    # render the template to update the data 
    return render_template('quest7_template_update_operation.html')

# add a route to perform actions for updating the details by fetching data form update form 
@app.route('/update', methods = ['POST'])
def update():
    # get employee id from form
    emp_id = request.form['emp_id']
    # get city from form
    city = request.form['city']
    # get country from form
    country = request.form['country']
    # connect with database
    with sqlite3.connect('database.db') as conn:
        print("Database is opened again")
        # start a try block to find exception
        try: 
            # create Cursor object using the cursor() method of the Connection object/class
            cur = conn.cursor()
            # update the employee details based on employee id
            cur.execute('UPDATE EMPLOYEE SET city = ?, country=? where e_id = ?',(city, country, emp_id))
            print(emp_id, city, country)
            # initialize a variable for successful updation
            msg = 'Updation is successful'
        # create an except block
        except:
            # rollback if there is an exception 
            conn.rollback()
            # initialize a variable for unsuccessful updation
            msg = 'Error in updation operation.'
        # create a finally block 
        finally : 
            # render a template for operation result page and  pass the msg
            return render_template('quest7_template_operation_result.html', msg = msg)
# create a route for showing the foge of record deletion
@app.route('/delete_employee')
def delete_details():
    # render the template for deletion operation
    return render_template('quest7_template_delete_operation.html')

# create a route to perform action for deletion operation by collecting data from deletion page
@app.route('/delete', methods = ['POST'])
def delete_employee():
    # get emp_id from form
    emp_id = request.form['emp_id']
    print(emp_id)
    # connect to database
    with sqlite3.connect('database.db') as conn:
        print("Database is opened again")
        # create a try block
        try: 
            # create Cursor object using the cursor() method of the Connection object/class
            cur = conn.cursor()
            # delete the record from employee table based on emp_id 
            cur.execute('DELETE FROM EMPLOYEE WHERE e_id = ?', (emp_id,))
            # commit the operation explicitly
            conn.commit()
            print(emp_id)
            # initialize a variable for successful deletion
            msg = 'Deletion is successful'
        # create a except block to catch error sqlite3.Error
        except sqlite3.Error as error:
            # rollback if there is an error
            conn.rollback()
            print(error)
            # initialize a variable for unsuccessful deletion
            msg = 'Error in deletion operation.'
        # create a finally block 
        finally : 
            # render template operation result 
            return render_template('quest7_template_operation_result.html', msg = msg)


# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)