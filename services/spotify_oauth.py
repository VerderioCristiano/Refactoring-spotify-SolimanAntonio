import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import session, redirect, url_for

# Configurazione delle credenziali di Spotify
SPOTIFY_CLIENT_ID = "d74cb805ae4f4e9c87c5d361d8adade3"
SPOTIFY_CLIENT_SECRET = "3a61d65da5914d1789080bccbc68e0fd"
SPOTIFY_REDIRECT_URI = "https://fuzzy-space-umbrella-5gqp7pj9vj5qfv7v4-5000.app.github.dev/callback"

# Scope dell'applicazione (permessi richiesti)
scope = "user-read-private playlist-read-private"

# Funzione per ottenere l'istanza di autenticazione di Spotify
def get_spotify_auth():
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=scope,
        show_dialog=True
    )

# Funzione per ottenere il client di Spotify con autenticazione opzionale
def get_spotify_client():
    token_info = session.get("token_info") # attraverso i token crea una connessione con le api di spotify

    if token_info:
        return spotipy.Spotify(auth=token_info.get("access_token"))  # Accesso autenticato
    
    return spotipy.Spotify(auth=None)