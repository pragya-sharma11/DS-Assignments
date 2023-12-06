# 1. Create a Flask app that displays "Hello, World!" on the homepage

# import the Flask, render_template, request from flask module
from flask import Flask, render_template, request
# create Flask application object in current module
app = Flask(__name__)
# create a route for page
@app.route('/')
def show_page():
    # return the page 
    return render_template('quest1_template.html')
# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)