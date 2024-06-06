from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3307/DnD-WBM'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class ModelUser:
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def login(user):
        found_user = ModelUser.get_by_username(user.username)
        if found_user and found_user.password == user.password:
            return found_user
        return None

@login_manager.user_loader
def load_user(user_id):
    return ModelUser.get_by_id(user_id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        logged_user = ModelUser.login(user)
        if logged_user:
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('El nombre de usuario o el correo electrónico ya están en uso')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado correctamente')
            return redirect(url_for('login'))
        except exc.SQLAlchemyError as err:
            flash('Error al registrar usuario: ' + str(err.__cause__))
    return render_template('auth/register.html')

@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    data = [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]
    return jsonify(data), 200

@app.route('/create_user', methods=['POST'])
def create_user():
    new_user = request.get_json()
    user = User(username=new_user['username'], email=new_user['email'], password=new_user['password'])
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Usuario creado correctamente'}), 201
    except exc.SQLAlchemyError as err:
        return jsonify({'message': 'Error al crear usuario: ' + str(err.__cause__)})

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
