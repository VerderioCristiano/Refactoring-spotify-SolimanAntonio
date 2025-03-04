from flask import Blueprint, render_template, request, session
from services.spotify_oauth import get_spotify_client

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=["GET", "POST"])
def home():
    sp = get_spotify_client()
    user_info, playlists = None, []

    if session.get("token_info"):
        try:
            user_info = sp.current_user()
            playlists = sp.current_user_playlists()["items"]
        except Exception:
            pass  

    search_results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            try:
                results = sp.search(q=query, type="playlist", limit=50)
                search_results = [
                    {
                        "id": playlist["id"],
                        "name": playlist.get("name", "Senza Nome"),
                        "owner": playlist["owner"].get("display_name", "Sconosciuto"),
                        "image": playlist["images"][0]["url"] if playlist.get("images") else None
                    }
                    for playlist in results.get("playlists", {}).get("items", [])
                    if playlist
                ]
            except Exception as e:
                print("Errore nella ricerca:", e)
    
    return render_template("home.html", user_info=user_info, playlists=playlists, query=query, search_results=search_results)

@home_bp.route("/playlist/<playlist_id>")
def playlist(playlist_id):
    sp = get_spotify_client()
    playlist_data, tracks = None, []
    try:
        playlist_data = sp.playlist(playlist_id)
        tracks_data = playlist_data["tracks"]["items"]
        tracks = [
            {
                "name": track["track"].get("name", "Senza Nome"),
                "artist": track["track"]["artists"][0].get("name", "Sconosciuto"),
                "album": track["track"]["album"].get("name", "Senza Nome"),
                "cover": track["track"]["album"].get("images", [{}])[0].get("url", None)
            }
            for track in tracks_data if track.get("track")
        ]
    except Exception as e:
        print("Errore nel recupero della playlist:", e)
    return render_template("playlist.html", playlist=playlist_data, tracks=tracks)
