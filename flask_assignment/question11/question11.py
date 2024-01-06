# 11. Create a real-time chat application using Flask-SocketIO.

# import random module
import random
# import ascii_uppercase from String module
from string import ascii_uppercase
# import everything inside flask module
from flask import * 
# import join_room, leave_room,  send,  SocketIO from flask_socketio module
from flask_socketio import join_room, leave_room,  send,  SocketIO

# create Flask application object in current module
app = Flask(__name__)
# add a secret key
app.config['SECRET_KEY'] = 'awehiuweh'
# set a bidirectional and event-based communication between a client and a server
socketio = SocketIO(app)

# create a dictionary for chat rooms 
rooms = {'default_pragya8326':{'members':0, 'messages':[]}}
# create a method to generate unique code for room
def generate_unique_code(length):
    # run a loop with True condition
    while True:
        # initialze a variable to store code
        code = ''
        # execute a loop for range length
        for i in range(length):
            # generate a random uppercase value and add it to code string
            code += random.choice(ascii_uppercase)
        # if code doesn't exist in room 
        if code not in rooms:
            break
    # return the random generated code 
    return code

# add a route for home page
@app.route('/')
def show_home():
    # render template for home page
    return render_template('home.html')

# add route for joining room
@app.route('/join_room', methods = ['POST'])
def go_to_room():
    # clear the initial session
    session.clear()
    name = request.form.get('name')
    # get() method returns value associated with 'name'. If no attribute named 'name' exists it returns None
    code = request.form.get('code')
    # get() method returns value associated with 'code'. If no attribute named 'code' exists it returns None
    join = request.form.get('join', False)
    # get() method returns value associated with 'join'. If no attribute named 'join' exists it returns False
    create = request.form.get('create', False)
    # get() method returns value associated with 'create'. If no attribute named 'create' exists it returns False
    

    # if join is True and code doesn't exist
    if join!=False and not code:
        # return home page template and paas name and code.
        return render_template('home.html', error = 'Please enter a room code.', name = name, code = code)
    
    # initialize room with code.
    room = code 
    # if create button is True and code 
    if create!=False and not code:
        # get a randome generated code
        room = generate_unique_code(5)
        # create a room with this randomly generated code.
        rooms[room] = {'members':0, 'messages':[]}
        print(room)
    # if code doesn't exists in rooms dictionary
    elif code not in rooms:
        # render tempalte and pass name and randomly generated room code
        return render_template('home.html', error = 'Room does not exist.', name = name, code = code)
    print(name, code, create, join, code not in rooms)
    # add name and code to session
    session['name'] = name 
    session['room'] = room
    # redirect the user to url of room
    return redirect(url_for('room'))
    # inside url_for() we pass function name for that route


# add route for room
@app.route('/room')
def room():
    # get room code from session
    room = session.get('room')
    print(room)
    # if room doesn't exist or name is none or room is not in rooms dictionary
    if room is None or session.get('name') is None or room not in rooms:
        # redirect user to home page
        return redirect(url_for('show_home'))
    # render tempalte of room page and pass code and messages
    return render_template('room.html', code=room, messages=rooms[room]["messages"])

# when user do message
@socketio.on("message")
def message(data):
    # get code of room
    room = session.get("room")
    # if room doesn't exist, return 
    if room not in rooms:
        return 
    # create a dictionary for name and messages
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    # send the content to room
    send(content, to=room)
    # append message and sender name to messages list of that room
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")


# on connection, perform the below operations
@socketio.on('connect')
def connect(auth):
    # get room code and name from session
    room = session.get('room')
    name = session.get('name')
    # if room is null or name is null then return
    if not room or not name:
        return
    # if room is not in rooms
    if room not in rooms:
        # leave room and return
        leave_room(room)
        return
    # if everything works fine, then join the room
    join_room(room)
    # send information to server
    send({"name": name, "message": "has entered the room"}, to=room)
    # increase members by 1
    rooms[room]['members'] += 1
    print(name, 'joined room', room)


# on disconnect, perform the below operations
@socketio.on('disconnect')
def disconnect():
    # get room code and name from session
    room = session.get('room')
    name = session.get('name')
    # leave the room
    leave_room(room)
    # if room in rooms dictionary
    if room in rooms:
        # decrease members by 1
        rooms[room]['members'] -= 1
        # if members in that room becomes 0 then delete the room
        if rooms[room]['members'] ==0:
            del rooms[room]
    # send infrmation to server
    send({"name":name, "message":"has left the room"}, to = room)
    print(name, 'left room', room)
    
# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    # app.run('0.0.0.0', port=5000)
    socketio.run(app, debug= True)