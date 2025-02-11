from flask import Blueprint, render_template, session, redirect, url_for, request
from services.spotify_oauth import get_spotify_client

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    sp = get_spotify_client()
    if isinstance(sp, str):  # Se il client restituisce un redirect, lo eseguiamo
        return sp

    user_info = sp.current_user()
    playlists = sp.current_user_playlists()["items"]

    playlist_id = request.args.get("playlist_id")
    tracks = []
    if playlist_id:
        tracks_data = sp.playlist_items(playlist_id)["items"]
        tracks = [
            {
                "name": track["track"]["name"],
                "artist": track["track"]["artists"][0]["name"],
                "album": track["track"]["album"]["name"],
                "cover": track["track"]["album"]["images"][0]["url"] if track["track"]["album"]["images"] else None
            }
            for track in tracks_data
        ]

    return render_template("home.html", user_info=user_info, playlists=playlists, tracks=tracks)
