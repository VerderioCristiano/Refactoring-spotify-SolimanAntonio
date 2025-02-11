import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import session, redirect, url_for

SPOTIFY_CLIENT_ID = "d74cb805ae4f4e9c87c5d361d8adade3"
SPOTIFY_CLIENT_SECRET = "3a61d65da5914d1789080bccbc68e0fd"
SPOTIFY_REDIRECT_URI = "https://turbo-guide-wr7jqjp4vp6xh9pqq-5000.app.github.dev/callback"

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
    if not token_info:
        return redirect(url_for("auth.login"))

    return spotipy.Spotify(auth=token_info["access_token"])
