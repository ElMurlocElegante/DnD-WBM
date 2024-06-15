from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    data = requests.get('http://localhost:5001/api/data').json()
    return render_template("home.html", data = data)

#Game rooms 

@app.route("/gameRooms")
def gameRooms(): #Get rooms API
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

#Room Creation

@app.route("/roomCreation")
def roomCreation():
    if ( session.get('user_id') is not None and session.get('username') is not None ):
        return render_template("createRoom.html")
    return redirect(url_for('login'))

#Characters

@app.route("/characters")
def characters(): #Character API
    if session.get('user_id') is not None and session.get('username') is not None:
        query = "SELECT * FROM `characters` WHERE `username` = :username"
        try:
            result = queryRead(query, {"username": session["username"]})
            characters = [dict(row._mapping) for row in result.fetchall()]
            return render_template("characters.html", data=characters)
        except SQLAlchemyError as err:
            return jsonify({'message': 'Se ha producido un error: ' + str(err.__cause__)})
    return redirect(url_for('login'))

#about

@app.route("/about")
def about():
    return render_template("about.html")

#Misc

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

#main

if __name__ == "__main__":
    app.run(port=5000)