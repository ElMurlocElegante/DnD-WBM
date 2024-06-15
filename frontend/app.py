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
    rooms = requests.get('http://localhost:5001/api/rooms').json()

    return render_template("rooms.html", rooms = rooms)

@app.route("/joinRoom", methods=['POST'])
def joinRoom():
    if request.method == 'POST':
        code = request.form['code']
        url = f'http://localhost:5001/api/join?code={code}'
        response = request.get(url)
        if response.status_code == 200:
            return redirect(url_for('room'))
        return redirect(url_for('gameRooms', ))
    
@app.route("/room")
def room():
    response = requests.get('http://localhost:5001/api/roomConnection')
    if response.status_code != 200:
        return redirect(url_for('home'))
    data = response.json()
    code = data.get('code')
    return render_template("room.html", code=code)

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