# 11. Create a real-time chat application using Flask-SocketIO.

import random
from string import ascii_uppercase
from flask import * 
from flask_socketio import join_room, leave_room,  send,  SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'awehiuweh'
socketio = SocketIO(app)

rooms = {'pragya8326':{'members':0, 'messages':[]}}
def generate_unique_code(length):
    while True:
        code = ''
        for i in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code

@app.route('/')
def show_home():
    return render_template('home.html')
@app.route('/join_room', methods = ['POST'])
def go_to_room():
    session.clear()
    name = request.form.get('name')
    # get() method returns value associated with 'name'. If no attribute named 'name' exists it returns None
    code = request.form.get('code')
    # get() method returns value associated with 'code'. If no attribute named 'code' exists it returns None
    join = request.form.get('join', False)
    # get() method returns value associated with 'join'. If no attribute named 'join' exists it returns False
    create = request.form.get('create', False)
    # get() method returns value associated with 'create'. If no attribute named 'create' exists it returns False
    
    if join!=False and not code:
        return render_template('home.html', error = 'Please enter a room code.', name = name, code = code)
    
    room = code 
    if create!=False and not code:
        room = generate_unique_code(5)
        rooms[room] = {'members':0, 'messages':[]}
        print(room)
    elif code not in rooms:
        return render_template('home.html', error = 'Room does not exist.', name = name, code = code)
    print(name, code, create, join, code not in rooms)
    session['name'] = name 
    session['room'] = room
    return redirect(url_for('room'))
    # inside url_for() we pass function name for that route

@app.route('/room')
def room():
    room = session.get('room')
    print(room)
    if room is None or session.get('name') is None or room not in rooms:
        return redirect(url_for('show_home'))
    return render_template('room.html', code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on('connect')
def connect(auth):
    room = session.get('room')
    name = session.get('name')
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]['members'] += 1
    print(name, 'joined room', room)

@socketio.on('disconnect')
def disconnect():
    room = session.get('room')
    name = session.get('name')
    leave_room(room)
    if room in rooms:
        rooms[room]['members'] -= 1
        if rooms[room]['members'] ==0:
            del rooms[room]
    send({"name":name, "message":"has left the room"}, to = room)
    print(name, 'left room', room)
    
# the below statement allows to Execute Code When the File Runs as a Script, 
# but Not When It's Imported as a Module.
if __name__ == '__main__':
    # run the application using run() method
    # app.run('0.0.0.0', port=5000)
    socketio.run(app, debug= True)