# 8. Implement user authentication and registration in a Flask app using Flask-Login.

from flask import * 
import flask_login
import sqlite3
app = Flask(__name__)
app.secret_key ='My Key'

login_manager = flask_login.LoginManager()
login_manager.init_app(app=app)

class User(flask_login.UserMixin):
    def __init__(self) -> None:
        super().__init__()
        self.id = None

@login_manager.user_loader
def user_loader(username):
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        row = cur.execute("SELECT * FROM LIVE_USERS where username = ?", (username,))
        row = row.fetchone()
        
        if row and username != row['username']  :
            return
    user = User()
    user.id = username
    return user 

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        row = cur.execute("SELECT * FROM LIVE_USERS where username = ?", (username,))
        row = row.fetchone()
        
        if row and username != row['username']  :
            return
    user = User()
    user.id = username
    return user 

@app.route('/')
def home_page():
    return render_template('quest8_template_homepage.html')

@app.route('/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM LIVE_USERS where username = ?", (username,))
        row = cur.fetchone()
        print((row['username'], row['password']) if row else 'None')
        if row and  username == row['username'] and password == row['password']:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return 'Logged in as: ' + flask_login.current_user.id +'<br> <a href="/logout">Log out</a>'
    return 'Account do not Exist with this username, <a href="/register_user">Create account</a>'

@app.route('/register_user')
def register_user():
    return render_template('quest8_template_register.html')

@app.route('/register', methods = ['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        row = cur.execute("SELECT * FROM LIVE_USERS where username = ?", (username,))
        row = row.fetchone()
        
        if row and username == row['username']  :
            return 'Account Existed with this username, please try with another username <a href="/register_user">Create account</a>'
        
        else:
            try: 
                cur = conn.cursor()
                cur.execute('INSERT into LIVE_USERS VALUES(?,?)',(username, password,))
                user = User()
                user.id = username
                flask_login.login_user(user)
                msg = 'Insertion is successful'
            except:
                conn.rollback()
                print('error')
                msg = 'Error in insertion operation.'
            finally : 
                return 'Registered as: ' + flask_login.current_user.id +'<br> <a href="/logout">Log out</a>'
            

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out <a href = "/">Login</a>'


# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)