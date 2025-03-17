from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models import db
from blueprints.auth import auth_bp
from blueprints.home import home_bp
from blueprints.spotify import spotify_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(spotify_bp)


@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)