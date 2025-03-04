from flask import Blueprint, jsonify, render_template
from services.spotify_oauth import get_random_playlists

playlist_bp = Blueprint("playlist", __name__)

@playlist_bp.route("/random_playlists", methods=["GET"])
def random_playlists():
    playlists = get_random_playlists()
    if "error" in playlists:
        return jsonify({"error": playlists["error"]}), 404
    return jsonify(playlists)

@playlist_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")