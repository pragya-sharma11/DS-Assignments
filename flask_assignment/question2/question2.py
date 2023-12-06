#2. Build a Flask app with static HTML pages and navigate between them.

# import the Flask, render_template, request from flask module
from flask import Flask, render_template, request
# create Flask application object in current module
app = Flask(__name__)
# create a route for page
@app.route('/page1')
def show_page1():
    # return the page 
    return render_template('quest2_template_a.html')

# create a route for page
@app.route('/page2')
def show_page2():
    # return the page 
    return render_template('quest2_template_b.html')


# create a route for page
@app.route('/page3')
def show_page3():
    # return the page 
    return render_template('quest2_template_c.html')


# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)