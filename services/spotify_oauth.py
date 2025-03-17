import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from flask import session, redirect, url_for, request, render_template
import random
SPOTIFY_CLIENT_ID = "d74cb805ae4f4e9c87c5d361d8adade3"
SPOTIFY_CLIENT_SECRET = "3a61d65da5914d1789080bccbc68e0fd"
SPOTIFY_REDIRECT_URI = "https://cuddly-invention-jj5wpwvgrv4j2556-5000.app.github.dev/callback"
SCOPE = "user-read-private playlist-read-private"

def get_spotify_auth():
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE,
        show_dialog=True
    )

def get_spotify_client():
    token_info = session.get("token_info")
    if token_info:
        return spotipy.Spotify(auth=token_info.get("access_token"))
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    ))

def get_random_playlists():
    sp = get_spotify_client()
    query = "music"
    results = sp.search(q=query, type="playlist", limit=50)
    playlists = results.get("playlists", {}).get("items", [])
    
    valid_playlists = []
    for playlist in playlists:
        if playlist:
            try:
                valid_playlists.append({
                    "title": playlist.get("name", "Senza titolo"),
                    "owner": playlist.get("owner", {}).get("display_name", "Sconosciuto"),
                    "url": playlist.get("external_urls", {}).get("spotify", "#"),
                    "image": playlist["images"][0]["url"] if playlist.get("images") else None
                })
            except Exception as e:
                print(f"Errore con la playlist: {e}, saltata.")
    
    return random.sample(valid_playlists, min(5, len(valid_playlists))) if valid_playlists else []

def search_playlists(query):
    sp = get_spotify_client()
    results = sp.search(q=query, type="playlist", limit=50)
    playlists = results.get("playlists", {}).get("items", [])
    return [
        {
            "title": playlist.get("name", "Senza titolo"),
            "owner": playlist.get("owner", {}).get("display_name", "Sconosciuto"),
            "url": playlist.get("external_urls", {}).get("spotify", "#"),
            "image": playlist["images"][0]["url"] if playlist.get("images") else None
        }
        for playlist in playlists if playlist
    ]

def get_playlist_tracks(playlist_id):
    sp = get_spotify_client()
    try:
        results = sp.playlist_tracks(playlist_id)
        tracks = [
            {
                "name": track["track"]["name"],
                "artist": ", ".join(artist["name"] for artist in track["track"]["artists"]),
                "album": track["track"]["album"]["name"],
                "url": track["track"]["external_urls"]["spotify"],
                "cover": track["track"]["album"]["images"][0]["url"] if track["track"]["album"]["images"] else None
            }
            for track in results["items"]
        ]
        return render_template("playlist.html", tracks=tracks)
    except Exception as e:
        print(f"Errore durante il recupero dei brani della playlist: {e}")
        return render_template("playlist.html", tracks=[], error="Impossibile recuperare i brani della playlist.")
    
def spotify_login():
    auth_manager = get_spotify_auth()
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)

def spotify_callback():
    auth_manager = get_spotify_auth()
    session["token_info"] = auth_manager.get_access_token(request.args.get("code"))
    return redirect(url_for("home"))

def get_user_playlists():
    sp = get_spotify_client()
    try:
        results = sp.current_user_playlists(limit=50)
        playlists = [
            {
                "name": playlist["name"],
                "owner": playlist["owner"]["display_name"],
                "url": playlist["external_urls"]["spotify"],
                "image": playlist["images"][0]["url"] if playlist["images"] else None
            }
            for playlist in results["items"]
        ]
        return playlists
    except Exception as e:
        print(f"Errore durante il recupero delle playlist personali: {e}")
    return[]