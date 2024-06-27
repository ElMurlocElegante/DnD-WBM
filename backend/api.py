from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_cors import CORS
from random import randint
import os
import json
import random
from string import ascii_uppercase

app = Flask(__name__)

engine = create_engine("mysql+mysqlconnector://root@localhost:3306/DnD-WBM")
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")
'''
///IMPORTANTE///
nombre DB: DnD-WBM
puerto: 3307 
///IMPORTANTE///
'''

#extras

@app.route('/api/roll_dice/<dice>')
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

#Rooms

@app.route("/api/rooms", methods = ['GET'])
def get_rooms():
    query = "SELECT room_creator, room_name, ingame, maxplayers FROM rooms;"
    result = queryRead(query)
    rooms = []
    for row in result:
        room = {}
        room["room_creator"] = row.room_creator
        room["room_name"] = row.room_name
        room["ingame"] = row.ingame
        room["maxplayers"] = row.maxplayers
        rooms.append(room)
    return jsonify(rooms)

@app.route("/api/join", methods = ['GET'])
def joinRoom():
    code = request.args.get('code')
    query = "SELECT ingame,maxplayers,code FROM rooms WHERE code = :code"
    result = queryRead(query, {"code": code})
    row = result.first()
    print(row)
    if row is not None and row[2] == code: 
        players = {}
        players['ingame'] = row[0]
        players['maxplayers'] = row[1]
        if (players['maxplayers'] > players['ingame']):
            return jsonify({"message": f'joining room with code: {code}'}), 200
        return jsonify({"message": "Room full"}), 401
    return jsonify({"message": "wrong code"}), 400

    
@app.route('/api/roomConnection', methods = ['GET'])
def roomConnection():
    room = request.args.get('room')
    query = "SELECT code FROM rooms;"
    result = queryRead(query)
    rooms = []
    for row in result:
        rooms.append(row.code)
    if room not in rooms:
        return jsonify({"message": "Error"}), 400
    return jsonify({"message": "Success", "code": room}), 200

@app.route('/api/rooms/create', methods=['POST'])
def roomCreation():
    data = request.get_json()
    code = codeGenerator(4)
    data["code"] = code
    query = "INSERT INTO rooms (room_creator, room_name, ingame, maxplayers, code) VALUES (:creatorName, :roomName, :ingame, :maxPlayers, :code)"
    result = queryCUD(query, {
                    'creatorName': data.get("creatorName"),
                    'roomName': data.get("roomName"),
                    'ingame': 0,
                    'maxPlayers': data.get("maxPlayers"),
                    'code': code
                })
    if result:
        return jsonify({"message": "Room created successfully", "code": code}), 200
    return jsonify({"message": "Error creating room"}), 400
    

#login

@app.route('/api/login', methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('user')
    password = data.get('password')
    query = "SELECT * FROM users WHERE username = :username AND password = :password;"
    result = queryRead(query,{"username": username, "password": password}).fetchone()
    if result:
        return jsonify({"message": "Login succesfull"}), 200
    return jsonify({"message": "Login failed"}), 401

#register

@app.route('/api/register', methods = ['POST'])
def register():
    data = request.get_json()
    username = data.get('user')
    password = data.get('password')
    email = data.get('email')
    query_email = "SELECT * FROM users WHERE email = :email;"
    query_username = "SELECT * FROM users WHERE username = :username;"
    result_email = queryRead(query_email,{"email": email}).fetchone()
    result_username = queryRead(query_username, {"username": username}).fetchone()
    if result_email:
        return jsonify({"message": "Email in use"}), 409
    if result_username:
        return jsonify({"message": "Username already in use"}), 409
    query = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password);"
    queryCUD(query, {"username": username, "email": email, "password": password})
    return jsonify({"message": "User registered"}), 200

#EDIT CHARACTERS
# Get character details by ID
@app.route('/api/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    query = "SELECT * FROM characters WHERE id = :character_id"
    result = queryRead(query, {"character_id": character_id}).fetchone()
    if result:
        return jsonify(dict(result._mapping)), 200
    return jsonify({"message": "Character not found"}), 404

# Update character details
@app.route('/api/character/edit', methods=['PATCH'])
def update_character():
    character_data = request.get_json()
    character_id = character_data.get('character_id')
    query_check = "SELECT * FROM characters WHERE id = :character_id"
    result_check = queryRead(query_check, {"character_id": character_id}).fetchone()
    if not result_check:
        return jsonify({"message": "Character not found"}), 404
    query_update = """
        UPDATE characters 
        SET 
            character_name = :character_name,
            class = :selectedClass,
            subclass = :selectedSubclass,
            background = :background,
            race = :race,
            alignment = :alignment,
            xp = :xp,
            hp = :hp,
            ac = :ac,
            strength = :strength,
            dexterity = :dexterity,
            constitution = :constitution,
            intelligence = :intelligence,
            wisdom = :wisdom,
            charisma = :charisma,
            proficiency_skills = :proficiency_skills,
            proficiency_n_language = :proficiency_n_language,
            equipment = :equipment,
            lore = :lore
        WHERE id = :character_id
    """
    params = {
        "character_id": character_id,
        "character_name": character_data.get("characterName"),
        "selectedClass": character_data.get("selectedClass"),
        "selectedSubclass": character_data.get("selectedSubclass"),
        "background": character_data.get("background"),
        "race": character_data.get("race"),
        "alignment": character_data.get("alignment"),
        "xp": character_data.get("xp"),
        "hp": character_data.get("hp"),
        "ac": character_data.get("ac"),
        "strength": character_data.get("strength"),
        "dexterity": character_data.get("dexterity"),
        "constitution": character_data.get("constitution"),
        "intelligence": character_data.get("intelligence"),
        "wisdom": character_data.get("wisdom"),
        "charisma": character_data.get("charisma"),
        "proficiency_skills": ','.join(character_data.get("skillProficiencies")),
        "proficiency_n_language": character_data.get("proficienciesLanguages"),
        "equipment": character_data.get("equipment"),
        "lore": character_data.get("lore")
    }
    try:
        result_update = queryCUD(query_update, params)
        if result_update:
            print(f"Updating character with ID {character_id}")
            print(f"Query: {query_update}")
            print(f"Params: {params}")

            # Debugging print for result_update
            print(f"Result update: {result_update}")
            return jsonify({"message": "Character updated successfully"}), 200
        else:
            return jsonify({"message": "Failed to update character"}), 400
    except Exception as e:
        return jsonify({"message": f"Failed to update character: {str(e)}"}), 500
    
# @app.route('/api/characters', methods = ['GET'])
# def get_characters():
#     username = request.args.get('user')
#     query = "SELECT * FROM characters WHERE username = :username"
#     result = queryRead(query, {"username": username})
#     characters = [dict(row._mapping) for row in result.fetchall()]
#     return jsonify(characters), 200

# characters 
@app.route('/api/characters', methods = ['GET'])
def get_characters():
    username = request.args.get('user')
    query = "SELECT * FROM `characters` WHERE `username` = :username"
    result = queryRead(query, {"username": username})
    characters = [dict(row._mapping) for row in result.fetchall()]
    return jsonify(characters), 200

@app.route("/api/index_data", methods=['GET'])
def getIndexData():
    index_route = os.path.join(app.root_path, 'data', 'class', 'index.json')
    if not os.path.exists(index_route):
        return jsonify({"error": "File Not Found, class index"}), 404
    with open(index_route, 'r') as json_file:
        classes = json.load(json_file)
    return jsonify(classes), 200

@app.route("/api/races_data", methods=['GET'])
def getRacesData():
    races_route = os.path.join(app.root_path, 'data', 'races.json')
    if not os.path.exists(races_route):
        return jsonify({"error": "File Not Found, races"}), 404
    with open(races_route, 'r') as json_file:
        race_details = [{"name": race['name'], "source": race['source']} for race in json.load(json_file)['race']]
    return jsonify(race_details), 200

@app.route("/api/backgrounds_data", methods=['GET'])
def getBackgroundsData():
    backgrounds_route = os.path.join(app.root_path, 'data', 'backgrounds.json')
    if not os.path.exists(backgrounds_route):
        return jsonify({"error": "File Not Found, backgrounds"})
    with open(backgrounds_route, 'r') as json_file:
        background_details = [{"name": background['name']} for background in json.load(json_file)['background']]
    return jsonify(background_details), 200


@app.route("/api/skills_data", methods=['GET'])
def getSkillData():
    skills_route = os.path.join(app.root_path, 'data', 'skills.json')
    if not os.path.exists(skills_route):
        return jsonify({"error": "File Not Found, skills"})
    with open(skills_route, 'r') as json_file:
        skills_details = [{"name": skill['name']} for skill in json.load(json_file)['skill']]
    return jsonify(skills_details), 200

@app.route("/api/delete_character/<string:username>/<int:character_id>", methods = ['DELETE'])
def deleteCharacter(username, character_id):
    query = "DELETE FROM characters WHERE username = :username AND id = :id"
    result = queryCUD(query, {"username": username, "id": character_id})
    if result:
        return jsonify({"message": "Character deleted successfully"}), 200
    return jsonify({"message": "character not found"}), 404

@app.route("/api/data/<string:jsonFile>", methods = ['GET'])
def getData(jsonFile):
    route = os.path.join(app.root_path, 'data', jsonFile)
    if not os.path.exists(route):
        return jsonify({"error": f"File Not Found: {jsonFile}"})
    with open(route, 'r') as json_file:
        return jsonify(json.load(json_file)), 200
    
@app.route("/api/data/class/<string:jsonFile>", methods = ['GET'])
def getClassData(jsonFile):
    route = os.path.join(app.root_path, 'data', 'class', jsonFile)
    if not os.path.exists(route):
        return jsonify({"error": f"File Not Found: {jsonFile}"})
    with open(route, 'r') as json_file:
        return jsonify(json.load(json_file)), 200
    
@app.route("/api/data/character/add", methods = ['POST'])
def addCharacter():
    data = request.get_json()
    query = """
        INSERT INTO characters (username, character_name, class, subclass, background, race, alignment, 
                                xp, hp, ac, strength, dexterity, constitution, intelligence, wisdom, charisma, 
                                proficiency_skills, proficiency_n_language, equipment, lore)
        VALUES (:username, :character_name, :class, :subclass, :background, :race, :alignment, 
                :xp, :hp, :ac, :strength, :dexterity, :constitution, :intelligence, :wisdom, :charisma, 
                :proficiency_skills, :proficiency_n_language, :equipment, :lore)
        """
    params = {
            "username": data.get("username"),
            "character_name": data.get("characterName"),
            "class": data.get("selectedClass"),
            "subclass": data.get("selectedSubclass"),
            "background": data.get("background"),
            "race": data.get("race"),
            "alignment": data.get("alignment"),
            "xp": data.get("xp"),
            "hp": data.get("hp"),
            "ac": data.get("ac"),
            "strength": data.get("strength"),
            "dexterity": data.get("dexterity"),
            "constitution": data.get("constitution"),
            "intelligence": data.get("intelligence"),
            "wisdom": data.get("wisdom"),
            "charisma": data.get("charisma"),
            "proficiency_skills": ','.join(data.get("skillProficiencies")),
            "proficiency_n_language": data.get("proficienciesLanguages"),
            "equipment": data.get("equipment"),
            "lore": data.get("lore")
        }
    result = queryCUD(query, params)
    if result:
        print(result)
        return jsonify({"message": "Character created correctly"}), 200
    return jsonify({"message": "Error creating character"}), 400


#delete account

@app.route("/api/delete_account/<string:username>", methods = ['DELETE'])
def deleteAccount(username):
    query_delete_characters = "DELETE FROM characters WHERE username = :username"
    query_delete_user = "DELETE FROM users WHERE username = :username"
    result_characters = queryCUD(query_delete_characters, {"username": username})
    result_user = queryCUD(query_delete_user, {"username": username})
    if result_characters and result_user:
        return jsonify({"message": "User deletes successfully"}), 200
    return jsonify({"message": "User not found"}), 404

#profile

@app.route("/api/userData", methods = ['GET'])
def getUserData():
    data = request.args.get('username')
    query = "SELECT email FROM users WHERE username = :username"
    result = queryRead(query, {'username': data})
    if result:
        for row in result:
            email = row.email
        return jsonify({'email': email}), 200
    return jsonify({"message": "User not found"}), 404

@app.route("/api/profile/changePassword", methods = ['POST'])
def checkPassword():
    data = request.get_json()
    password = data['password']
    username = data['user']
    newPassword = data['newPassword']
    query = "SELECT password FROM users WHERE username = :username"
    result = queryRead(query, {'username': username})
    if result:
        for row in result:
            originalPassword = row.password
        if originalPassword == password:
            query = "UPDATE users SET password = :password WHERE username = :username"
            queryCUD(query, {"password": newPassword,
                             "username": username})
            return jsonify({"message": "password changed correctly"}), 200
        return jsonify({"message": "Passwords do not match"}), 401
    return jsonify({"message": "Denied"}), 400

#socket io

@socketio.on("connect")
def connect():

    data = request.args.get('session')

    sessionData = json.loads(data)

    print(data)

    room = sessionData['room']
    name = sessionData['username']

    query = "SELECT code FROM rooms;"
    result = queryRead(query)
    rooms = []
    for row in result:
        rooms.append(row.code)

    if room not in rooms:
        leave_room(room)
        return
    join_room(room)
    send({"name": name, "message": "Has entered the room"}, to=room)

    query = "UPDATE rooms SET ingame = ingame + 1 WHERE code = :code"
    result = queryCUD(query, {"code": room})

    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():

    data = request.args.get('session')

    sessionData = json.loads(data)

    room = sessionData['room']
    name = sessionData['username']

    query = "SELECT code FROM rooms;"
    result = queryRead(query)
    rooms = []
    for row in result:
        rooms.append(row.code)

    leave_room(room)
    if room in rooms:
        query = "UPDATE rooms SET ingame = ingame - 1 WHERE code = :code"
        result = queryCUD(query, {"code": room})
        
        query = "SELECT ingame FROM rooms WHERE code = :code" 
        result = queryRead(query, {"code": room})
        
        for row in result:
            ingame = row.ingame

        if ingame <= 0:
            query = "DELETE FROM rooms WHERE code = :code"
            result = queryCUD(query, {"code": room})

    
    send({"name": name, "message": "Has left the room"}, to=room)
    print(f"{name} left room {room}")

@socketio.on("message")
def message(data):

    dataJson = request.args.get('session')

    sessionData = json.loads(dataJson)

    room = sessionData['room']
    name = sessionData['username']

    query = "SELECT code FROM rooms;"
    result = queryRead(query)

    rooms = []
    for row in result:
        rooms.append(row.code)
    if room not in rooms:
        return
    content = {
        "name": name,
        "message": data["data"]
    }
    send(content, to=room)
    print(f"{name} said: {data['data']}")

#main

if __name__ == "__main__":
    socketio.run(app, port=5001)