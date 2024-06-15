from flask import Flask,jsonify, request, session, flash
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
app.config['SECRET_KEY'] = 'SECRET'
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})
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

@app.route("/api/data")
def data():
    return {"message": "hello from backend"}

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
def join_room():
    code = request.args.get('code')
    session["room"] = code
    query = "SELECT ingame,maxplayers FROM rooms WHERE code = :code"
    result = queryRead(query, {"code": code})
    players = {}
    row = result.first()
    players['ingame'] = row[0]
    players['maxplayers'] = row[1]
    if (players['maxplayers'] > players['ingame']):
        return jsonify({"message": f'joining room with code: {code}'}), 200
    return jsonify({"message": "room full"}), 400

@app.route('/api/check_login', methods=['GET'])
def check_login():
    if 'user_id' in session and 'username' in session:
        return jsonify({'logged_in': True}), 200
    else:
        return jsonify({'logged_in': False}), 400
    
@app.route('/api/roomConnection')
def roomConnection():
    room = session.get("room")
    query = "SELECT code FROM rooms;"
    result = queryRead(query)
    rooms = []
    for row in result:
        rooms.append(row.code)
    if room is None or session.get("username") is None or room not in rooms:
        return jsonify({"message": "error"}), 400
    return jsonify({"message": "success", "code": room}), 200

if __name__ == "__main__":
    socketio.run(app, port=5001)