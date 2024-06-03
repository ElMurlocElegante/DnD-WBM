from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
import json

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


if __name__ == "__main__":
    app.run("127.0.0.1", port=5000, debug=True)