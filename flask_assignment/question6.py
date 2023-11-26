# 6. Build a Flask app that allows users to upload files and display them on the website.

# import the Flask, render_template from flask module
from flask import *
import urllib.request
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/'

# create Flask application object in current module
app = Flask(__name__)
app.secret_key = 'hello'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024*1024
allowed_extensions = set(['png','jpeg','jpg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# add the route for a page
@app.route('/show') # / to show it on home location  -> url+port -> home location
def show():
    return render_template('quest6_template.html')

@app.route('/show', methods = ['POST'])
def show_file():
    if 'file1' not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files['file1']
    if file.filename == '':
        flash("No image selected for uploading")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file.save(UPLOAD_FOLDER+ filename)
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('quest6_template.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)

    return redirect(url_for('show',filename='../uploads/' + filename), code=301)
# 'sdfghj'
# redirect(url_for( filename='uploads/' + filename), code=301)
 
    
    # # get the information from file input field with name as 'file1'
    # f = request.files['file1']
# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)