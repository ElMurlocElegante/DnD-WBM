from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET'

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
        session["room"] = code
        url = f'http://localhost:5001/api/join?code={code}'
        response = request.get(url)
        if response.status_code == 200:
            return redirect(url_for('room'))
        return redirect(url_for('gameRooms', ))
    
@app.route("/room")
def room():
    room = session.get("room")
    url = f'http://localhost:5001/api/roomConnection?room={room}'
    response = requests.get(url)
    if response.status_code != 200 or room is None or session.get("username") is None:
        return redirect(url_for('home'))
    return render_template("room.html", code=room)

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
            username = session['username']
            url = f'http://localhost:5001/api/characters?user={username}'
            characters = requests.get(url).json()         
            return render_template("characters.html", data=characters)
    return redirect(url_for('login'))

#login

@app.route('/check_login', methods=['GET'])
def check_login():
    if 'user_id' in session and 'username' in session:
        return jsonify({'logged_in': True})
    else:
        return jsonify({'logged_in': False})

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = {
            "user": username,
            "password": password
        }
        response = requests.post('http://localhost:5001/api/login', json=data)
        if response.status_code == 200:
            data = response.json()
            id = data.get('user_id')
            session['user_id'] = id
            session['username'] = username
            return redirect(url_for('characters'))
        else:
            flash('Usuario o contraseña incorrecta', 'danger')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

#register

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        data = {
            "user": username,
            "password": password,
            "email": email
        }
        response = requests.post('http://localhost:5001/api/register', json=data)
        if response.status_code == 200:
            flash(response.json()['message'], 'success')
            return redirect(url_for('login'))
        flash(response.json()['message'], 'danger')
        return render_template('auth/register.html')
    else:
        return render_template('auth/register.html')
            

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