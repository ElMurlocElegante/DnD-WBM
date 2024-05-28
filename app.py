from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root@localhost:3307/DnD-WBM") 
'''
///IMPORTANTE///
nombre DB: DnD-WBM
puerto: 3307 
///IMPORTANTE///
'''
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/characters", methods=['GET'])
def characters():
    return render_template("characters.html")

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
if __name__ == "__main__":
    app.run("127.0.0.1", port=5000, debug=True)