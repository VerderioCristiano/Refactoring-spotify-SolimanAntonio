import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import session, redirect, url_for

SPOTIFY_CLIENT_ID = "d74cb805ae4f4e9c87c5d361d8adade3"
SPOTIFY_CLIENT_SECRET = "3a61d65da5914d1789080bccbc68e0fd"
SPOTIFY_REDIRECT_URI = "https://bug-free-chainsaw-jj5wpwvgrvx7c4p9-5000.app.github.dev/callback"

scope = "user-read-private playlist-read-private"

def get_spotify_auth():
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=scope,
        show_dialog=True
    )



def get_spotify_client():
    token_info = session.get("token_info") 

    if token_info:
        return spotipy.Spotify(auth=token_info.get("access_token"))
    
    return spotipy.Spotify(auth=None)