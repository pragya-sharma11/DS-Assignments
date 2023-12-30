# 10. Design a Flask app with proper error handling for 404 and 500 errors.

from flask import * 
app = Flask(__name__)

# @app.route('/')
# def show_home():
#     return render_template('quest10_home.html')
@app.route('/form_page')
def show_form_page():
    return render_template('quest10_form.html')
@app.route('/data_page', methods = ['POST'])
def show_data_page():
    fn = request.form['firstname']
    ln = request.form['lastname']
    return render_template('quest10_data.html', data = {'firstname':fn , 'lastname':ln})
@app.errorhandler(404)
def error_404(e):
    return render_template('quest10_error.html', msg = 'This page is not currently available')

@app.errorhandler(500)
def internal_error(e):
    return render_template('quest10_error.html', msg = 'Sorry, There is some issue. Please try later')


# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)