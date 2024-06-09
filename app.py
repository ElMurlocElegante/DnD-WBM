from flask import Flask, jsonify, request, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from flask_socketio import SocketIO, join_room, leave_room, send
import os
import json
import random
from string import ascii_uppercase






app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root@localhost:3306/DnD-WBM")
app.config['SECRET_KEY'] = 'SECRET'
socketio = SocketIO(app)
'''
///IMPORTANTE///
nombre DB: DnD-WBM
puerto: 3307 
///IMPORTANTE///
'''

def codeGenerator(lenght):

    try:
        conn = engine.connect()
        query = "SELECT code FROM rooms;"
        result = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    codes = []
    for row in result:
        codes.append(row.code)

    while True:
        code = ""
        for _ in range(lenght):
            code += random.choice(ascii_uppercase)
        if code not in codes:
            break
    return code

@app.route("/")
def home():
    session.clear()
    return render_template("home.html")

@app.route("/characters", methods=['GET'])
def characters():
    index_route = os.path.join(app.root_path, 'data', 'class', 'index.json')
    races_route = os.path.join(app.root_path, 'data', 'races.json')
    backgrounds_route = os.path.join(app.root_path, 'data', 'backgrounds.json')
    skills_route = os.path.join(app.root_path, 'data', 'skills.json')

    if not os.path.exists(index_route):
        return jsonify({"error": "File Not Found, class index"}), 404

    if not os.path.exists(races_route):
        return jsonify({"error": "File Not Found, races"}), 404
    
    if not os.path.exists(backgrounds_route):
        return jsonify({"error": "File Not Found, backgrounds"})
    
    if not os.path.exists(skills_route):
        return jsonify({"error": "File Not Found, skills"})
    
    with open(index_route, 'r') as json_file:
        classes = json.load(json_file)

    with open(races_route, 'r') as json_file:
        race_details = [{"name": race['name'], "source": race['source']} for race in json.load(json_file)['race']]
    
    with open(backgrounds_route, 'r') as json_file:
        background_details = [{"name": background['name']} for background in json.load(json_file)['background']]

    with open(skills_route, 'r') as json_file:
        skills_details = [{"name": skill['name']} for skill in json.load(json_file)['skill']]

    return render_template("create-character.html",classes=classes, races=race_details, backgrounds=background_details, skills=skills_details)

@app.route("/characters/delete_character", methods=['DELETE'])
def delete_character(character_name):
    return redirect(url_for('characters'))

@app.route("/characters/add_character", methods=['POST'])
def add_character():
    conn = engine.connect()
    new_character = request.get_json()
    try:
        character_name = request.form.get('character_name')
        class_name = request.form.get('class')
        xp = request.form.get('xp')
        hp = request.form.get('hp')
        alignment = request.form.get('alignment')
        background = request.form.get('background')
        race = request.form.get('race')
        ac = request.form.get('ac')
        strength = request.form.get('strength')
        dexterity = request.form.get('dexterity')
        constitution = request.form.get('constitution')
        intelligence = request.form.get('intelligence')
        wisdom = request.form.get('wisdom')
        charisma = request.form.get('charisma')
        personality_traits = request.form.get('personality_traits')
        ideals = request.form.get('ideals')
        bonds = request.form.get('bonds')
        flaws = request.form.get('flaws')
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    return redirect(url_for('characters'))

@app.route("/battle_manager")
def battle_manager():
    return render_template("battle_manager.html")

@app.route("/github")
def github():
    return redirect("https://github.com/ElMurlocElegante/DnD-WBM")

@app.route("/data/<json_file>")
def get_data(json_file):
    file_path = f"data/{json_file}"
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                return jsonify(json.load(file))
        except FileNotFoundError:
            return jsonify({"error": f"{json_file} file not found"})
    else:
        return jsonify({"error": f"{json_file} not found"})

@app.route("/data/class/<json_file>")
def get_class_data(json_file):
    file_path = f"data/class/{json_file}"
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                return jsonify(json.load(file))
        except FileNotFoundError:
            return jsonify({"error": f"{json_file} file not found"})
    else:
        return jsonify({"error": f"{json_file} not found"})
    
@app.route("/gameRooms")
def gameRooms():

    try:
        conn = engine.connect()
        query = "SELECT room_creator, room_name, ingame, maxplayers FROM rooms;"
        result = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    rooms = []
    for row in result:
        room = {}
        room["room_creator"] = row.room_creator
        room["room_name"] = row.room_name
        room["ingame"] = row.ingame
        room["maxplayers"] = row.maxplayers
        rooms.append(room)

    return render_template("rooms.html", rooms = rooms)

@app.route("/joinRoom", methods=['POST'])
def joinRoom():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        session["room"] = code
        session["name"] = name
        return redirect(url_for('room'))


@app.route("/roomCreation")
def roomCreation():
    return render_template("createRoom.html")

@app.route("/room")
def room():
    room = session.get("room")
    try:
        conn = engine.connect()
        query = "SELECT code FROM rooms;"
        result = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    rooms = []
    for row in result:
        rooms.append(row.code)

    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for('home'))
    return render_template("room.html", code=room)

@app.route("/roomCreated", methods=['POST'])
def roomCreated():
    if request.method == 'POST':
        roomName = request.form['roomName']
        creatorName = request.form['creatorName']
        maxPlayers = request.form['maxPlayers']
        code = codeGenerator(4)

        try:
            conn = engine.connect()
            query = text("""INSERT INTO rooms (room_creator, room_name, ingame, maxplayers, code)
                            VALUES (:creatorName, :roomName, :ingame, :maxPlayers, :code)""")
            conn.execute(query, {
                'creatorName': creatorName,
                'roomName': roomName,
                'ingame': 0,
                'maxPlayers': maxPlayers,
                'code': code
            })
            conn.commit()
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))

        session["room"] = code
        session["name"] = creatorName
        return redirect(url_for('room'))

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")

    try:
        conn = engine.connect()
        query = "SELECT code FROM rooms;"
        result = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    rooms = []
    for row in result:
        rooms.append(row.code)

    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)

    try:
        conn = engine.connect()
        query = text("UPDATE rooms SET ingame = ingame + 1 WHERE code = '"+ room +"';")
        result = conn.execute(query, {'code': room})
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))

    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")

    try:
        conn = engine.connect()
        query = "SELECT code FROM rooms;"
        result = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    rooms = []
    for row in result:
        rooms.append(row.code)

    leave_room(room)
    if room in rooms:

        try:
            conn = engine.connect()
            query = f"UPDATE rooms SET ingame = ingame - 1 WHERE code = '{room}';"
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))

        
        try:
            conn = engine.connect()
            query = "SELECT ingame FROM rooms WHERE code = '"+ room +"';" 
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
        
        for row in result:
            ingame = row.ingame

        if ingame <= 0:

            try:
                conn = engine.connect()
                query = f"""DELETE FROM rooms WHERE code = '{room}';"""
                result = conn.execute(text(query))
                conn.commit()
                conn.close()
            except SQLAlchemyError as err:
                jsonify(str(err.__cause__))

    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} left room {room}")

@socketio.on("message")
def message(data):
    room = session.get("room")
    try:
        conn = engine.connect()
        query = "SELECT code FROM rooms;"
        result = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    rooms = []
    for row in result:
        rooms.append(row.code)
    if room not in rooms:
        return
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    print(f"{session.get('name')} said: {data['data']}")


if __name__ == "__main__":
    socketio.run(app, debug=True)