from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    playlists = db.relationship('UserPlaylist', backref='user', lazy=True)

class Playlist(db.Model):
    id = db.Column(db.String(150), primary_key=True)  
    name = db.Column(db.String(150), nullable=False)
    owner = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(300), nullable=True)

class UserPlaylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    playlist_id = db.Column(db.String(150), db.ForeignKey('playlist.id'), nullable=False)