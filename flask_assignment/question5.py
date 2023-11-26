# 5. Implement user sessions in a Flask app to store and display user-specific data.

# import the Flask, render_template from flask module
from flask import Flask, request, render_template, session, redirect, url_for
# create Flask application object in current module
app = Flask(__name__)
# give a secret key for the session
app.secret_key = 'hello'
# add the route for a page
@app.route('/login') 
def show_form():
    # using this function, you will be able to showcase your html files
    return render_template('quest5_template_a.html')

# add a route to direct the user to another page for showing result
@app.route('/get_data', methods = ['POST'])
# create a function
def get_data():
    # get the username from the form shown on page using get() method of request method
    username = request.form.get('username')
    # get the username from the form shown on page using get() method of request method
    password = request.form.get('password')
    session['username'] = username
    session['password'] = password
    # return  to the next page
    return redirect(url_for("user_page"))

# add the route for a page to logout
@app.route('/logout_data', methods = ['POST'])
def logout():
    # if username exists in session
    if "username" in session:
        # remove the data from session
        session.pop("username")
        session.pop('password')
    # redirect the flow of execution to the login page
    return redirect(url_for('login'))
    
# add the route for a page
@app.route('/user_page')
def user_page():
    # if username exists in session
    if "username" in session:
        # then get the values from session
        username = session['username']
        password = session['password']
        # render the second template and pass data to the html page
        return render_template('quest5_template_b.html', data={'username' : username, 'password':password})
    # otherwose return the login form
    else:
        return redirect(url_for('login'))

# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port = 5001)