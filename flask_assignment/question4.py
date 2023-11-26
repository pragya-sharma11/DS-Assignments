# 4. Create a Flask app with a form that accepts user input and displays it.
# import the Flask, render_template from flask module
from flask import Flask, request, render_template
# create Flask application object in current module
app = Flask(__name__)
# add the route for a page
@app.route('/') # / to show it on home location  -> url+port -> home location
def show_form():
    # using this function, you will be able to showcase your html files
    return render_template('quest4_template.html')
    
# add a route to direct the user to another page for showing result
@app.route('/check_password', methods = ['POST'])
# create a function
def check_password():
    # get the username from the form shown on page using get() method of request method
    username = request.form.get('username')
    # get the username from the form shown on page using get() method of request method
    password = request.form.get('password')
    # return the data to the page
    return f"username {username} and password {password} received"
# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port = 5000)