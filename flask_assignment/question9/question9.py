# 9. Create a RESTful API using Flask to perform CRUD operations on resources like books or movies.

from flask import * 
app = Flask(__name__)

# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    app.run('0.0.0.0', port=5000)