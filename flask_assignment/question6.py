# 6. Build a Flask app that allows users to upload files and display them on the website.

# import the Flask, render_template from flask module
from flask import *
from werkzeug.utils import secure_filename
# initialize a variable to store folder path of images
UPLOAD_FOLDER = 'uploads/'

# create Flask application object in current module
app = Flask(__name__, static_folder=UPLOAD_FOLDER)
# add a secret key
app.secret_key = 'hello'
# allowed extensions for images
allowed_extensions = set(['png','jpeg','jpg','gif'])

# create a method to check if image has valid extension or nor
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# add the route for a page
@app.route('/show') # / to show it on home location  -> url+port -> home location
def show():
    # render the template
    return render_template('quest6_template.html')

# add a route to post the file values
@app.route('/show', methods = ['POST'])
def show_file():
    print("File post method")
    # if file not in request.files
    if 'file1' not in request.files:
        # redirect to request.url 
        flash("No file part")
        return redirect(request.url)
    # get the file from the source page
    file = request.files['file1']
    # if file does not exist then redirect to source page
    if file.filename == '':
        flash("No image selected for uploading")
        return redirect(request.url)
    # if file existed and extension is valid 
    if file and allowed_file(file.filename):
        # secure the file using secure_filename() method
        filename = secure_filename(file.filename)
        flash('Image successfully uploaded and displayed below')
        # render the same source template and pass the name of file
        return render_template('quest6_template.html', filename=filename)
    # else rdirect to same source page
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
#  create a route to show image on webpage
@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    # redirect page with the image by sending the whole path of file 
    return redirect(url_for('static',filename='../uploads/'+filename), code=301)

# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)