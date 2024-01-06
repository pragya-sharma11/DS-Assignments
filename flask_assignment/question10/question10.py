# 10. Design a Flask app with proper error handling for 404 and 500 errors.

# import everything 
from flask import * 
# create Flask application object in current module
app = Flask(__name__)

# create a route for form page
@app.route('/form_page')
def show_form_page():
    # render the template quest10_form.html 
    return render_template('quest10_form.html')

# add a route to direct the user to another page
@app.route('/data_page', methods = ['POST'])
def show_data_page():
    # get first name from form
    fn = request.form['firstname']
    # get last name from form
    ln = request.form['lastname']
    # render the template quest10_data.html and pass data values for first name and last name
    return render_template('quest10_data.html', data = {'firstname':fn , 'lastname':ln})
# handle the error using errorhandler for 404 error
@app.errorhandler(404)
def error_404(e):
    # render the template quest10_error.html and pass message value to this page
    return render_template('quest10_error.html', msg = 'This page is not currently available')
# handle the error using errorhandler for 500 error
@app.errorhandler(500)
def internal_error(e):
    # render the template quest10_error.html and pass message value to this page
    return render_template('quest10_error.html', msg = 'Sorry, There is some issue. Please try later')


# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)