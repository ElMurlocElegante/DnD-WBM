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
        
        query = "SELECT * FROM users WHERE email = :email;"
        conn = engine.connect()
        try:
            result = conn.execute(text(query), {"email": email}).fetchone()
            if result:
                flash('El correo ya está en uso', 'danger')
                conn.close()
                return render_template('auth/register.html')
            
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
    session.clear()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('login'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = engine.connect()
    query = f"DELETE FROM users WHERE id = {user_id};"
    try:
        conn.execute(text(query))
        conn.commit()
        conn.close()
        session.clear()
        flash('Cuenta eliminada correctamente', 'success')
    except SQLAlchemyError as err:
        flash(f"Error: {str(err.__cause__)}", 'danger')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run("127.0.0.1", port=5000, debug=True)
