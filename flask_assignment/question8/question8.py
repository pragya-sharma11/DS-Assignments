# 8. Implement user authentication and registration in a Flask app using Flask-Login.

# import everything from flask module
from flask import * 
# import flask_login module
import flask_login
# import sqlite3 for database connection
import sqlite3
# create Flask application object in current module
app = Flask(__name__)
# add a secret key to the app
app.secret_key ='My Key'

# create an object for LoginManager
login_manager = flask_login.LoginManager()
# initialize the loginmanager with the app
login_manager.init_app(app=app)

# create a class named User that inherits UserMixin class from flask_login module
class User(flask_login.UserMixin):
    def __init__(self) -> None:
        super().__init__()
        self.id = None

# This callback is used to reload the user object from the user ID stored in the storage db.
@login_manager.user_loader
def user_loader(username):
    # connect with the database
    with sqlite3.connect('database.db') as conn:
        # get a row_factory to inspect the rquery result and prepare a callable 
        conn.row_factory = sqlite3.Row
        # create Cursor object using the cursor() method of the Connection object/class
        cur = conn.cursor()
        # get all the records from the table Live_users based on username
        row = cur.execute("SELECT * FROM LIVE_USERS where username = ?", (username,))
        # fetch one record from above result
        row = row.fetchone()
        # if row exists and username is not matched with username present in that row then return
        if row and username != row['username']  :
            return
    # create a User object 
    user = User()
    # put username in id variable of user object
    user.id = username
    # return that object
    return user 

# This sets the callback for loading a user from a Flask request. 
# The function you set should take Flask request object and return a user object or None if the user does not exist.
@login_manager.request_loader
def request_loader(request):
    # get the username from form
    username = request.form.get('username')
    # connect with the database 
    with sqlite3.connect('database.db') as conn:
        # get a row_factory to inspect the rquery result and prepare a callable 
        conn.row_factory = sqlite3.Row
        # create Cursor object using the cursor() method of the Connection object/class
        cur = conn.cursor()
        # get all the records from the table Live_users based on username
        row = cur.execute("SELECT * FROM LIVE_USERS where username = ?", (username,))
        # fetch one record from above result
        row = row.fetchone()
        
        # if row exists and username is not matched with username present in that row then return
        if row and username != row['username']  :
            return
    # create a User object 
    user = User()
    # put username in id variable of user object
    user.id = username
    # return that object
    return user 

# create a route for homepage
@app.route('/')
def home_page():
    # render template for home page
    return render_template('quest8_template_homepage.html')

# create a route for performing action on login form
@app.route('/login', methods = ['POST'])
def login():
    # get username from form
    username = request.form['username']
    # get password from form
    password = request.form['password']
    # connect with database
    with sqlite3.connect('database.db') as conn:
        # get a row_factory to inspect the rquery result and prepare a callable 
        conn.row_factory = sqlite3.Row
        # create Cursor object using the cursor() method of the Connection object/class
        cur = conn.cursor()
        # get all the records from the table Live_users based on username
        cur.execute("SELECT * FROM LIVE_USERS where username = ?", (username,))
        # fetch one record from above result
        row = cur.fetchone()
        print((row['username'], row['password']) if row else 'None')
        # if row exists and username and password matched to row data
        if row and  username == row['username'] and password == row['password']:
            # create object for this user
            user = User()
            # # put username in id variable of user object
            user.id = username
            # login the user though this object
            flask_login.login_user(user)
            # return a dummy page with some info
            return 'Logged in as: ' + flask_login.current_user.id +'<br> <a href="/logout">Log out</a>'
    # return that the account does not exists msg
    return 'Account do not Exist with this username, <a href="/register_user">Create account</a>'

# create a route for registering a user
@app.route('/register_user')
def register_user():
    # render a template to register the user
    return render_template('quest8_template_register.html')

# create a route for performing action on register form
@app.route('/register', methods = ['POST'])
def register():
    # get username form form
    username = request.form['username']
    # get username form form
    password = request.form['password']
    # connect with database
    with sqlite3.connect('database.db') as conn:
        # get a row_factory to inspect the rquery result and prepare a callable 
        conn.row_factory = sqlite3.Row
        # create Cursor object using the cursor() method of the Connection object/class
        cur = conn.cursor()
        # select all the records where username matches with form's username
        row = cur.execute("SELECT * FROM LIVE_USERS where username = ?", (username,))
        # get one of those rows
        row = row.fetchone()
        # if there is a row existed and username matches with the username of row
        if row and username == row['username']  :
            # user is already existed so return an appropriate message
            return 'Account Existed with this username, please try with another username <a href="/register_user">Create account</a>'
        # when row doesn't existed
        else:
            # start a try block
            try: 
                # create Cursor object using the cursor() method of the Connection object/class
                cur = conn.cursor()
                # insert a new record with username and password 
                cur.execute('INSERT into LIVE_USERS VALUES(?,?)',(username, password,))
                # create object of User class
                user = User()
                # create id of User with username
                user.id = username
                # login the user
                flask_login.login_user(user)
                # initialize a variable with successful insertion message
                msg = 'Insertion is successful'
            # create a except block
            except:
                # if there is an exception then rollback the operation
                conn.rollback()
                print('error')
                # initialize a variable with unsuccessful insertion message
                msg = 'Error in insertion operation.'
            finally : 
                # return the page to show current user login with logout link
                return 'Registered as: ' + flask_login.current_user.id +'<br> <a href="/logout">Log out</a>'
            
# create route for logout 
@app.route('/logout')
def logout():
    # logout the user
    flask_login.logout_user()
    # return the page with login link
    return 'Logged out <a href = "/">Login</a>'


# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000, debug=True)