from flask import Flask,jsonify, request, session, flash
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

engine = create_engine("mysql+mysqlconnector://root@localhost:3306/DnD-WBM")
app.config['SECRET_KEY'] = 'SECRET'
socketio = SocketIO(app)
'''
///IMPORTANTE///
nombre DB: DnD-WBM
puerto: 3307 
///IMPORTANTE///
'''

@app.route("/api/data")
def data():
    return {"message": "hello from backend"}

if __name__ == "__main__":
    socketio.run(app, port=5001)