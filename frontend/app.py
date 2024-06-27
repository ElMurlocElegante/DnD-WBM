from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import requests, json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET'

@app.route("/")
def home():
    return render_template("home.html")

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
        response = requests.get(url)
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
    if check_login()[1] == 200:
        return render_template("createRoom.html")
    return redirect(url_for('login'))

@app.route("/roomCreated", methods=['POST'])
def roomCreated():
    if request.method == 'POST':
        roomName = request.form['roomName']
        creatorName = session.get('username')
        maxPlayers = request.form['maxPlayers']
        data = {
            "roomName": roomName,
            "creatorName": creatorName,
            "maxPlayers": maxPlayers
        }
        response = requests.post('http://localhost:5001/api/rooms/create', json=data)
        if response.status_code == 200:
            data = response.json()
            session['room'] = data.get('code')
            return redirect(url_for('room'))
        flash(response.json()['message'], 'danger')
        return redirect(url_for('roomCreation'))
    return redirect(url_for('home'))

#EDIT CHRARACTERS
@app.route('/character/edit', methods=['GET', 'PATCH'])
def edit_character():
    if request.method == 'PATCH':
        # Handling the form submission to update the character
        character_data = request.get_json()
        response = requests.patch(f'http://localhost:5001/api/character/edit', json=character_data)
        if response.status_code == 200:
            flash('Character updated successfully!', 'success')
            return jsonify({"message": "success"}), 200
        else:
            flash('Failed to update character.', 'danger')
            return jsonify({"message": "error updating character"}), 400
    else:
        # Handling the form display to edit the character
        character_id = request.args.get('character_id')
        if not character_id:
            flash('Character ID is required.', 'danger')
            return redirect(url_for('characters'))
        response = requests.get(f'http://localhost:5001/api/character/{character_id}')
        if response.status_code == 200:
            character = response.json()
            equipment_str = character['equipment']
            equipment_json = json.loads(equipment_str)
            character['equipment'] = equipment_json
            lore_str = character['lore']
            profs_n_lang_str = character['proficiency_n_language']
            lore_json = json.loads(lore_str)
            profs_n_lang_json = json.loads(profs_n_lang_str)
            character['lore'] = lore_json
            character['proficiency_n_language'] = profs_n_lang_json
            classes = requests.get('http://localhost:5001/api/index_data').json()
            races = requests.get('http://localhost:5001/api/races_data').json()
            backgrounds = requests.get('http://localhost:5001/api/backgrounds_data').json()
            skills = requests.get('http://localhost:5001/api/skills_data').json()
            return render_template("edit-character.html", character=character, classes=classes, races=races, backgrounds=backgrounds, skills=skills)
        else:
            flash('Character not found.', 'danger')
            return redirect(url_for('characters'))


#Characters

@app.route("/characters")
def characters():
    if check_login()[1] == 200:
            username = session['username']
            url = f'http://localhost:5001/api/characters?user={username}'
            characters = requests.get(url).json()         
            return render_template("characters.html", data=characters)
    return redirect(url_for('login'))

@app.route("/character/create", methods=['GET'])
def createCharacter():
    classes = requests.get('http://localhost:5001/api/index_data').json()
    race_details = requests.get('http://localhost:5001/api/races_data').json()
    background_details = requests.get('http://localhost:5001/api/backgrounds_data').json()
    skills_details = requests.get('http://localhost:5001/api/skills_data').json()
    return render_template("create-character.html",classes=classes, races=race_details, backgrounds=background_details, skills=skills_details)

@app.route('/character/delete', methods=['POST'])
def delete_character():
    username = session['username']
    character_id = request.form.get('character_id')
    if not character_id:
        flash('Character ID is required.', 'danger')
        return redirect(url_for('characters'))
    url = f"http://localhost:5001/api/delete_character/{username}/{character_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        flash(response.json()['message'], 'success')
    else:
        flash(response.json()['message'], 'danger')
    return redirect(url_for('characters'))

@app.route("/character/add", methods = ['POST'])
def addCharacter():
    if check_login()[1] == 200:
        character_data = request.get_json()
        character_data["username"] = session['username']
        response = requests.post("http://localhost:5001/api/data/character/add", json=character_data)
        if response.status_code == 200:
            return jsonify({"message": "success"}), 200
        return jsonify({"message": "error creating character"}), 400
    return jsonify({"message": "not logged in"}), 401

#profile

@app.route("/profile")
def profile():
    if check_login()[1] == 200:
        username = session['username']
        response = requests.get("http://localhost:5001/api/userData", params={'username': username})
        data = response.json()
        email = data['email']
        userData = {
            "username": username,
            "email": email
        }
        return render_template("profile.html", data=userData)
    return redirect(url_for('home'))

@app.route("/change_password", methods = ['POST'])
def changePassword():
    currentPass = request.form['currentPassword']
    newPass = request.form['newPassword']
    mainData = {"password": currentPass,
                "user": session['username'],
                "newPassword": newPass}
    response = requests.post("http://localhost:5001/api/profile/changePassword", json=mainData)
    if response.status_code == 200:
        flash(response.json()['message'], 'success')
        return redirect(url_for('profile'))
    flash(response.json()['message'], 'danger')
    return redirect(url_for('profile'))



#login

@app.route('/check_login', methods=['GET'])
def check_login():
    if 'username' in session:
        return jsonify({'logged_in': True}), 200
    else:
        return jsonify({'logged_in': False}), 401

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
            session['username'] = username
            return redirect(url_for('characters'))
        else:
            flash('Incorrect user or password', 'danger')
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

#logout

@app.route('/logout')
def logout():
    session.clear()
    flash('Session successufully closed', 'success')
    return render_template("home.html")

#delete account

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if check_login()[1] == 200:
        username = session['username']
        url = f"http://localhost:5001/api/delete_account/{username}"
        response = requests.delete(url)
        if response.status_code == 200:
            session.clear()
            return redirect(url_for('login'))
        return redirect(url_for('characters'))
    return redirect(url_for('login'))

           

#about

@app.route("/about")
def about():
    return render_template("about.html")

#Misc

@app.route("/session", methods = ['GET'])
def getSessionData():
    data = {
        "username": session['username'],
        "room": session['room']
    }
    return jsonify(data)

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