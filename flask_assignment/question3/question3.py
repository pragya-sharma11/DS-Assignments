# 3. Develop a Flask app that uses URL parameters to display dynamic content.

# import the Flask, render_template, request from flask module
from flask import Flask, render_template, request
# create Flask application object in current module
app = Flask(__name__)
# add the route for a page
@app.route('/user')
def print_user():
    # get the parameter data of parameter 'name' from url 
    data = request.args.get('name')
    # return it on page body
    return f"{data}" 

# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)