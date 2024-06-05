from flask import Flask, jsonify, request, render_template, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_mysqldb import MySQL
import os
import json
import random
from string import ascii_uppercase

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root@localhost:3306/DnD-WBM")
app.config['SECRET_KEY'] = 'SECRET'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gamerooms'
mysql = MySQL(app) 
socketio = SocketIO(app)
'''
///IMPORTANTE///
nombre DB: DnD-WBM
puerto: 3307 
///IMPORTANTE///
'''

def codeGenerator(lenght):
    cur = mysql.connection.cursor()
    cur.execute('SELECT code FROM rooms ')
    rooms = [row[0] for row in cur.fetchall()]
    while True:
        code = ""
        for _ in range(lenght):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
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

    return render_template("characters.html",classes=classes, races=race_details, backgrounds=background_details, skills=skills_details)

@app.route("/characters/delete_character", methods=['DELETE'])
def delete_character(character_name):
    return redirect(url_for('characters'))

@app.route("/characters/add_character", methods=['POST'])
def add_character(character_name):
    return redirect(url_for('characters'))

@app.route("/battle_manager")
def battle_manager():
    return render_template("battle_manager.html")

@app.route("/github")
def github():
    return redirect("https://github.com/ElMurlocElegante/DnD-WBM")

@app.route("/data/backgrounds.json")
def get_backgrounds():
    try:
        with open('data/backgrounds.json','r') as json_file:
            return jsonify(json.load(json_file))
    except FileNotFoundError:
        return jsonify({"error": "Backgrounds file not found"})
    

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
    cur = mysql.connection.cursor()
    cur.execute('SELECT room_creator, room_name, ingame, maxplayers FROM rooms ')
    rooms = cur.fetchall()
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
    cur = mysql.connection.cursor()
    cur.execute('SELECT code FROM rooms ')
    rooms = [row[0] for row in cur.fetchall()]
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for('home'))
    return render_template("room.html")

@app.route("/roomCreated", methods=['POST'])
def roomCreated():
    if request.method == 'POST':
        roomName = request.form['roomName']
        creatorName = request.form['creatorName']
        maxPlayers = request.form['maxPlayers']
        code = codeGenerator(4)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO rooms (room_creator, room_name, ingame, maxplayers, code) VALUES (%s, %s, %s, %s, %s)', (creatorName, roomName, 0, maxPlayers, code))
        mysql.connection.commit()
        session["room"] = code
        session["name"] = creatorName
        return redirect(url_for('room'))

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    cur = mysql.connection.cursor()
    cur.execute('SELECT code FROM rooms ')
    rooms = [row[0] for row in cur.fetchall()]
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    cur.execute(f"UPDATE rooms SET ingame = ingame + 1 WHERE code = '{room}'")
    mysql.connection.commit()
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    cur = mysql.connection.cursor()
    cur.execute('SELECT code FROM rooms ')
    rooms = [row[0] for row in cur.fetchall()]
    leave_room(room)
    if room in rooms:
        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE rooms SET ingame = ingame - 1 WHERE code = '{room}'")
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT ingame FROM rooms WHERE code = '{room}'")
        ingame = [row[0] for row in cur.fetchall()]
        if ingame[0] <= 0:
            cur = mysql.connection.cursor()
            cur.execute(f"DELETE FROM rooms WHERE code = '{room}'")
            mysql.connection.commit()
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} left room {room}")
        

if __name__ == "__main__":
    socketio.run(app, debug=True)