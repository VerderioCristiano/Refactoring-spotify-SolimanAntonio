from flask import Blueprint, render_template, session, redirect, url_for, request
from services.spotify_oauth import get_spotify_client
import spotipy

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    sp = get_spotify_client()
    if not isinstance(sp, spotipy.Spotify):
        return sp  # Redirect response

    try:
        user_info = sp.current_user()
        playlists = sp.current_user_playlists()["items"]
    except Exception:
        return redirect(url_for("auth.login"))

    playlist_id = request.args.get("playlist_id")
    tracks = []
    if playlist_id:
        tracks_data = sp.playlist_items(playlist_id)["items"]
        tracks = [
            {
                "name": track["track"]["name"],
                "artist": track["track"]["artists"][0]["name"],
                "album": track["track"]["album"]["name"],
                "cover": track["track"]["album"].get("images", [{}])[0].get("url")
            }
            for track in tracks_data if track.get("track")
        ]

    return render_template("home.html", user_info=user_info, playlists=playlists, tracks=tracks)
