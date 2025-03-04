import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from flask import session
import random

SPOTIFY_CLIENT_ID = "d74cb805ae4f4e9c87c5d361d8adade3"
SPOTIFY_CLIENT_SECRET = "3a61d65da5914d1789080bccbc68e0fd"
SPOTIFY_REDIRECT_URI = "https://opulent-journey-v6v7j795p5qg3x5q-5000.app.github.dev/callback"
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
        if playlist:  # Controlla che la playlist non sia None
            try:
                valid_playlists.append({
                    "title": playlist.get("name", "Senza titolo"),
                    "owner": playlist.get("owner", {}).get("display_name", "Sconosciuto"),
                    "url": playlist.get("external_urls", {}).get("spotify", "#"),
                    "image": playlist["images"][0]["url"] if playlist.get("images") else None
                })
            except Exception as e:
                print(f"Errore con la playlist: {e}, saltata.")
    
    return random.sample(valid_playlists, min(5, len(valid_playlists))) if valid_playlists else {"error": "Nessuna playlist valida trovata"}