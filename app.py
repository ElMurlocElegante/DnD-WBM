from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = 'qwerty'  
engine = create_engine("mysql+mysqlconnector://root@localhost:3307/DnD-WBM")

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "SELECT * FROM users WHERE username = :username AND password = :password;"
        conn = engine.connect()
        try:
            result = conn.execute(text(query), {"username": username, "password": password}).fetchone()
            conn.close()
        except SQLAlchemyError as err:
            flash(f"Error: {str(err.__cause__)}", 'danger')
            return render_template('auth/login.html')
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

        # Verificar si el correo ya existe en la base de datos
        query = "SELECT * FROM users WHERE email = :email;"
        conn = engine.connect()
        try:
            result = conn.execute(text(query), {"email": email}).fetchone()
            if result:
                flash('El correo ya está en uso', 'danger')
                conn.close()
                return render_template('auth/register.html')

            # Insertar el nuevo usuario en la base de datos
            query = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password);"
            conn.execute(text(query), {"username": username, "email": email, "password": password})
            conn.commit()
            conn.close()
            flash('Usuario registrado correctamente', 'success')
            return redirect(url_for('login'))
        except SQLAlchemyError as err:
            flash(f"Error: {str(err.__cause__)}", 'danger')
            return render_template('auth/register.html')
    else:
        return render_template('auth/register.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session.get('username'))
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    data = [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]
    return jsonify(data), 200

@app.route('/users/<id>', methods=['PATCH'])
def update_user(id):
    mod_user = request.get_json()
    user = User.query.get(id)
    if user:
        user.username = mod_user.get('username', user.username)
        user.email = mod_user.get('email', user.email)
        try:
            db.session.commit()
            return jsonify({'message': 'Usuario actualizado correctamente'}), 200
        except exc.SQLAlchemyError as err:
            return jsonify({'message': 'Error al actualizar usuario: ' + str(err.__cause__)})
    return jsonify({'message': 'Usuario no encontrado'}), 404

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        data = {'id': user.id, 'username': user.username, 'email': user.email}
        return jsonify(data), 200
    return jsonify({'message': 'Usuario no encontrado'}), 404

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'Usuario eliminado correctamente'}), 202
        except exc.SQLAlchemyError as err:
            return jsonify({'message': 'Error al eliminar usuario: ' + str(err.__cause__)})
    return jsonify({'message': 'Usuario no encontrado'}), 404

if __name__ == '__main__':
    app.run("127.0.0.1", port=5000, debug=True)
