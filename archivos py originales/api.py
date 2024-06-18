from flask import Flask, jsonify, request, render_template, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from flask_socketio import SocketIO, join_room, leave_room, send
from random import randint
import os
import json
import random
from string import ascii_uppercase

app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root@localhost:3307/DnD-WBM")
app.config['SECRET_KEY'] = 'SECRET'
socketio = SocketIO(app)

def queryRead(query, args=None):
    if args:
        try:
            conn = engine.connect()
            result = conn.execute(text(query), args)
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
    else:
        try:
            conn = engine.connect()
            result = conn.execute(text(query))
            conn.close()
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
    return result

def queryCUD(query, args):
    try:
        conn = engine.connect()
        result = conn.execute(text(query), args)
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    return result

def codeGenerator(lenght):
    
    result = queryRead("SELECT code FROM rooms;")
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

@app.route('/check_login', methods=['GET'])
def check_login():
    if 'user_id' in session and 'username' in session:
        return jsonify({'logged_in': True})
    else:
        return jsonify({'logged_in': False})
    
@app.route("/characters/add_character", methods=['POST'])
def add_character():
    if ( session.get('user_id') is not None and session.get('username') is not None ):
        character_data = request.json  # Obtener los datos JSON del cuerpo de la solicitud
        query = """
        INSERT INTO characters (username, character_name, class, subclass, background, race, alignment, 
                                xp, hp, strength, dexterity, constitution, intelligence, wisdom, charisma, 
                                proficiency_skills, proficiency_n_language, equipment, lore)
        VALUES (:username, :character_name, :class, :subclass, :background, :race, :alignment, 
                :xp, :hp, :strength, :dexterity, :constitution, :intelligence, :wisdom, :charisma, 
                :proficiency_skills, :proficiency_n_language, :equipment, :lore)
        """
        params = {
            "username": session["username"],
            "character_name": character_data["characterName"],
            "class": character_data["className"],
            "subclass": character_data.get("subclassName"),
            "background": character_data["background"],
            "race": character_data["race"],
            "alignment": character_data["alignment"],
            "xp": character_data["xp"],
            "hp": character_data["hp"],
            "strength": character_data["strength"],
            "dexterity": character_data["dexterity"],
            "constitution": character_data["constitution"],
            "intelligence": character_data["intelligence"],
            "wisdom": character_data["wisdom"],
            "charisma": character_data["charisma"],
            "proficiency_skills": ','.join(character_data["skillProficiencies"]),
            "proficiency_n_language": character_data.get("proficienciesLanguages"),
            "equipment": character_data.get("equipment"),
            "lore": character_data["lore"]
        }

        try:
            result = queryCUD(query, params)
            return jsonify({'message': 'Character added successfully.'}), 201
        except SQLAlchemyError as err:
            return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})
    else:
        return jsonify({"message": "    Not Logged In"}), 400
    
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

@app.route('/roll_dice/<dice>')
def roll_dice(dice):
    if dice.startswith("d"):
        if dice[1:].isdigit():
            num_caras = int(dice[1:])
            resultado = randint(1, num_caras)
            return jsonify({"resultado": resultado, "total": resultado})
    elif "d" in dice:
        num_dados, num_caras = dice.split("d")
        if num_dados.isdigit() and num_caras.isdigit():
            num_dados = int(num_dados)
            num_caras = int(num_caras)
            if num_dados > 0 and num_caras > 0:
                resultados = [randint(1, num_caras) for _ in range(num_dados)]
                total = 0
                for result in resultados:
                    total += result
                return jsonify({"resultados": resultados, "total": total})
    return jsonify({"error": "Formato de dice incorrecto. Debe ser 'dn' o 'ndn', donde 'n' es un número mayor que cero."}), 400

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("username")

    try:
        query = "SELECT code FROM rooms;"
        result = queryRead(query)
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
        query = "UPDATE rooms SET ingame = ingame + 1 WHERE code = :code"
        result = queryCUD(query, {"code": room})
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))

    print(f"{name} joined room {room}") 

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("username")

    try:
        query = "SELECT code FROM rooms;"
        result = queryRead(query)
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    rooms = []
    for row in result:
        rooms.append(row.code)

    leave_room(room)
    if room in rooms:

        try:
            query = "UPDATE rooms SET ingame = ingame - 1 WHERE code = :code"
            result = queryCUD(query, {"code": room})
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))

        
        try:
            query = "SELECT ingame FROM rooms WHERE code = :code" 
            result = queryRead(query, {"code": room})
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
        
        for row in result:
            ingame = row.ingame

        if ingame <= 0:

            try:
                query = "DELETE FROM rooms WHERE code = :code"
                result = queryCUD(query, {"code": room})
            except SQLAlchemyError as err:
                jsonify(str(err.__cause__))

    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} left room {room}")

@socketio.on("message")
def message(data):
    room = session.get("room")
    try:
        query = "SELECT code FROM rooms;"
        result = queryRead(query)
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    rooms = []
    for row in result:
        rooms.append(row.code)
    if room not in rooms:
        return
    content = {
        "name": session.get("username"),
        "message": data["data"]
    }
    send(content, to=room)
    print(f"{session.get('username')} said: {data['data']}")

if __name__ == "__main__":
    socketio.run(app, debug=True)