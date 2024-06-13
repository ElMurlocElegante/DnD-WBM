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
'''
///IMPORTANTE///
nombre DB: DnD-WBM
puerto: 3307 
///IMPORTANTE///
'''

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

@app.route("/")
def home():
    return render_template("home.html")

# Account Things


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "SELECT * FROM users WHERE username = :username AND password = :password;"
        result = queryRead(query,{"username": username, "password": password}).fetchone()
        if result:
            session['user_id'] = result.id  
            session['username'] = result.username 
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrecta', 'danger')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        query_email = "SELECT * FROM users WHERE email = :email;"
        query_username = "SELECT * FROM users WHERE username = :username;"
        try:
            result = queryRead(query_email,{"email": email}).fetchone()
            if result:
                flash('El correo ya está en uso', 'danger')
                return render_template('auth/register.html')
            result_username = queryRead(query_username, {"username": username}).fetchone()
            if result_username:
                flash('El nombre de usuario ya está en uso', 'danger')
                return render_template('auth/register.html')
            query = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password);"
            queryCUD(query, {"username": username, "email": email, "password": password})
            flash('Usuario registrado correctamente', 'success')
            return redirect(url_for('login'))
        except SQLAlchemyError as err:
            flash(f"Error: {str(err.__cause__)}", 'danger')
            return render_template('auth/register.html')
    else:
        return render_template('auth/register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'success')
    return render_template("home.html")

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    query = "DELETE FROM users WHERE id = :id"
    try:
        queryCUD(query, {"id": user_id})
        session.clear()
        flash('Cuenta eliminada correctamente', 'success')
    except SQLAlchemyError as err:
        flash(f"Error: {str(err.__cause__)}", 'danger')
    
    return redirect(url_for('login'))

@app.route('/check_login', methods=['GET'])
def check_login():
    if 'user_id' in session and 'username' in session:
        return jsonify({'logged_in': True})
    else:
        return jsonify({'logged_in': False})

@app.route("/characters")
def characters():
    if session.get('user_id') is not None and session.get('username') is not None:
        query = "SELECT * FROM `characters` WHERE `username` = :username"
        try:
            result = queryRead(query, {"username": session["username"]})
            characters = [dict(row._mapping) for row in result.fetchall()]
            return render_template("characters.html", data=characters)
        except SQLAlchemyError as err:
            return jsonify({'message': 'Se ha producido un error: ' + str(err.__cause__)})
    return redirect(url_for('login'))

@app.route("/create_character", methods=['GET'])
def createCharacter():
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

@app.route('/delete_character', methods=['POST'])
def delete_character():
    username = session['username']
    character_id = request.form.get('character_id')  # Cambiado a 'character_id' para reflejar el nombre correcto
    if not character_id:
        flash('Character ID is required.', 'danger')
        return redirect(url_for('characters'))

    query = "DELETE FROM characters WHERE username = :username AND id = :id"
    try:
        result = queryCUD(query, {"username": username, "id": character_id})
        if isinstance(result, str):  # Si hay un error
            flash(f"Error: {result}", 'danger')
        else:
            flash('Character deleted successfully.', 'success')
    except SQLAlchemyError as err:
        flash(f"Database error: {str(err.__cause__)}", 'danger')
    return redirect(url_for('characters'))

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
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/github/<profile>/<repo>")
@app.route("/github/<profile>")
def github_redirect(profile, repo=None):
    if repo:
        return redirect(f"https://github.com/{profile}/{repo}")
    else:
        return redirect(f"https://github.com/{profile}")

@app.route("/ig/<profile>")
def instagram_redirect(profile):
    return redirect (f"https://www.instagram.com/{profile}/")

@app.route("/socketio")
def socketio_redirect():
    return redirect("https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js")

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
  
@app.route("/gameRooms")
def gameRooms():
    try:
        query = "SELECT room_creator, room_name, ingame, maxplayers FROM rooms;"
        result = queryRead(query)
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
        code = request.form['code']
        session["room"] = code

        try:
            query = "SELECT ingame,maxplayers FROM rooms WHERE code = :code"
            result = queryRead(query, {"code": code})
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))
        players = {}
        row = result.first()
        players['ingame'] = row[0]
        players['maxplayers'] = row[1]
        if (players['maxplayers'] > players['ingame']):
            return redirect(url_for('room'))
        
        try:
            query = "SELECT room_creator, room_name, ingame, maxplayers FROM rooms;"
            result = queryRead(query)
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

        return render_template("rooms.html", rooms=rooms, data="sala llena")
        


@app.route("/roomCreation")
def roomCreation():
    if ( session.get('user_id') is not None and session.get('username') is not None ):
        return render_template("createRoom.html")
    return redirect(url_for('login'))

@app.route("/room")
def room():
    room = session.get("room")
    try:
        query = "SELECT code FROM rooms;"
        result = queryRead(query)
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    rooms = []
    for row in result:
        rooms.append(row.code)

    if room is None or session.get("username") is None or room not in rooms:
        return redirect(url_for('home'))
    return render_template("room.html", code=room)

@app.route("/roomCreated", methods=['POST'])
def roomCreated():
    if request.method == 'POST':
        roomName = request.form['roomName']
        creatorName = session.get('username')
        maxPlayers = request.form['maxPlayers']
        code = codeGenerator(4)

        try:
            query = "INSERT INTO rooms (room_creator, room_name, ingame, maxplayers, code) VALUES (:creatorName, :roomName, :ingame, :maxPlayers, :code)"
            queryCUD(query, {
                'creatorName': creatorName,
                'roomName': roomName,
                'ingame': 0,
                'maxPlayers': maxPlayers,
                'code': code
            })
        except SQLAlchemyError as err:
            return jsonify(str(err.__cause__))

        session["room"] = code
        return redirect(url_for('room'))

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