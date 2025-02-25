from flask import Blueprint, jsonify, render_template
import requests
import random
import base64


SPOTIFY_CLIENT_ID = "d74cb805ae4f4e9c87c5d361d8adade3"
SPOTIFY_CLIENT_SECRET = "3a61d65da5914d1789080bccbc68e0fd"

playlist_bp = Blueprint("playlist", __name__)


def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta del token: {e}")
        return None


def get_random_playlists():
    access_token = get_access_token()
    if not access_token:
        return {"error": "Impossibile ottenere il token di accesso"}

    query = "music" 
    api_url = f"https://api.spotify.com/v1/search?q={query}&type=playlist&limit=50"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  
        data = response.json()

        playlists = data.get("playlists", {}).get("items", [])
        if not playlists:
            return {"error": "Nessuna playlist trovata"}

    
        valid_playlists = []
        for playlist in playlists:
            try:
                title = playlist.get("name", "Senza titolo")
                owner = playlist.get("owner", {}).get("display_name", "Sconosciuto")
                url = playlist.get("external_urls", {}).get("spotify", "#")
                image = playlist["images"][0]["url"] if playlist.get("images") else None

                valid_playlists.append({
                    "title": title,
                    "owner": owner,
                    "url": url,
                    "image": image,
                })
            except Exception as e:
                print(f"Errore con la playlist: {e}, saltata.")

        if not valid_playlists:
            return {"error": "Nessuna playlist valida trovata"}

        
        return random.sample(valid_playlists, min(5, len(valid_playlists)))

    except requests.exceptions.RequestException as e:
        print(f"Errore API Spotify: {e}")
        return {"error": "Errore nella comunicazione con Spotify"}
    except Exception as e:
        print(f"Errore generico: {e}")
        return {"error": "Errore sconosciuto"}


@playlist_bp.route("/random_playlists", methods=["GET"])
def random_playlists():
    return jsonify(get_random_playlists())


@playlist_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")
