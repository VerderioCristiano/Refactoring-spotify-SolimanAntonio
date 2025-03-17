from flask import Flask, redirect, render_template, url_for, session
from flask_login import LoginManager, current_user
from services.autenticazione import register, login, home, logout
from services.spotify_oauth import spotify_login, spotify_callback, get_playlist_tracks, get_user_playlists, get_random_playlists
from models import db, User

app = Flask(__name__)
app.secret_key = 'your_secret_key'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.add_url_rule('/', 'index', lambda: redirect(url_for('login')))
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/home', 'home', home, methods=['GET'])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/spotify_login', 'spotify_login', spotify_login)
app.add_url_rule('/callback', 'spotify_callback', spotify_callback)
app.add_url_rule('/playlist/<playlist_id>', 'playlist', get_playlist_tracks, methods=['GET'])

@app.route('/my_playlists')
def my_playlists():
    
    if 'token_info' not in session:
        return redirect(url_for('spotify_login'))  
    playlists = get_user_playlists()  
    return render_template('my_playlists.html', playlists=playlists)

@app.route('/random_playlists')
def random_playlists():
    playlists = get_random_playlists()  
    return render_template('home.html', username=current_user.username, playlists=playlists)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)