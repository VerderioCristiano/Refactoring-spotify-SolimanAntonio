from flask import Blueprint, render_template, session
from blueprints.authf import get_spotify_client
import spotipy

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    sp = get_spotify_client()

    user_info, playlists = None, []
    try:
        if isinstance(sp, spotipy.Spotify):  # Controllo se ho un client valido
            user_info = sp.current_user()
            playlists = sp.current_user_playlists()["items"]
    except Exception:
        pass  # Se l'utente non è autenticato, non mostriamo nulla

    return render_template("home.html", user_info=user_info, playlists=playlists)


@home_bp.route("/playlist/<playlist_id>")
def playlist(playlist_id):
    sp = get_spotify_client()

    playlist_data, tracks = None, []
    try:
        if isinstance(sp, spotipy.Spotify):
            playlist_data = sp.playlist(playlist_id)
            tracks_data = playlist_data["tracks"]["items"]
            tracks = [
                {
                    "name": track["track"]["name"],
                    "artist": track["track"]["artists"][0]["name"],
                    "album": track["track"]["album"]["name"],
                    "cover": track["track"]["album"].get("images", [{}])[0].get("url")
                }
                for track in tracks_data if track.get("track")
            ]
    except Exception:
        pass  # Se c'è un errore, lasciamo la pagina vuota o con un messaggio

    return render_template("playlist.html", playlist=playlist_data, tracks=tracks)