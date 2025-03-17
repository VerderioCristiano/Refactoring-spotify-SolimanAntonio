from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Questo username è già in uso.")

        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)  
            return redirect(url_for('home.home'))
        except Exception as e:
            db.session.rollback()
            return render_template('register.html', error=f"Errore durante la registrazione: {e}")
    return render_template('register.html', error=None)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home.home'))

        return render_template('login.html', error="Credenziali non valide.")
    return render_template('login.html', error=None)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))