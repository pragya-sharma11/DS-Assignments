# 12. Build a Flask app that updates data in real-time using WebSocket connections.

# import everything from flask module 
from flask import * 
# import emit and socketIO from flask_socketio module
from flask_socketio import emit, SocketIO
# import json
import json 

# instantiate the object of Flask class
app = Flask(__name__)
# assign a secret key
app.config['SECRET_KEY'] = 'awehiuweh'
# set a bidirectional and event-based communication between a client and a server
socketio = SocketIO(app)

# on connect event
@socketio.on('connect')
def we_connect():
    # create a try block
    try: 
        # open the file in read mode 
        f =  open("test.txt", 'r') 
        # read the file
        data = f.read()
        # get the value from json key - counter and add 1 in it
        val = int(json.loads(data).get("counter"))+int(1)
        # create a dict with updated value of counter
        temp = {'counter':val}
        # close the file object
        f.close()
        # open file in write format
        f =  open("test.txt", 'w', encoding='utf-8') 
        # dump the dict in json format in file
        f.write(json.dumps(temp))
        # close the file
        f.close()
        # emit the event operation  on user with broadcast flag as true
        emit('user', temp, broadcast=True)
    # create an except block to catch exceptions
    except Exception as e :
        # open file in write mode
        f =  open("test.txt", 'w', encoding='utf-8') 
        # dump the json data with counter value as 0
        f.write(json.dumps({"counter":0}))
        # close the file
        f.close()
        # emit the event operation  on user with broadcast flag as true
        emit('user', {"counter":0}, broadcast=True)

# on disconnect event
@socketio.on('disconnect')
def we_disconnect():
    # open file in read format
    f =  open("test.txt", 'r') 
    # read the file
    data = f.read()
    # get the value from json key - counter and subtract 1 in it
    temp = {'counter':int(json.loads(data).get("counter"))-1}
    # close the file
    f.close()
    # open file in write format
    f =  open("test.txt", 'w', encoding='utf-8') 
    # dump the dict in json format in file
    f.write(json.dumps(temp))
    print(temp)
    # close the file
    f.close()
    # emit the event operation  on user with broadcast flag as true
    emit('user',temp, broadcast=True)

# create a route for hoempage
@app.route('/', methods = ['POST', 'GET'])
def show_home():
    # open file in read format
    f =  open("test.txt", 'r')
    # read the data 
    data = f.read()
    # create a dict with value of counter
    temp = {'counter':int(json.loads(data).get("counter"))}
    # close the file 
    f.close()
    # render the template of home page and pass json data temp 
    return render_template('home.html', data = temp)

#  the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    # app.run('0.0.0.0', port=5000)
    socketio.run(app, debug= True)