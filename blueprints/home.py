from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from services.spotify_oauth import search_playlists, get_random_playlists
from services.analisi import analyze_and_visualize  

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
@login_required
def home():
    query = request.args.get("query")
    playlists = search_playlists(query) if query else get_random_playlists()
    return render_template('home.html', username=current_user.username, playlists=playlists)

@home_bp.route('/playlist/<playlist_id>')
@login_required
def playlist(playlist_id):
    
    from services.spotify_oauth import get_playlist_tracks
    tracks = get_playlist_tracks(playlist_id)
    
    if not tracks:
        return render_template('playlist.html', error="Nessun brano trovato.", playlist_id=playlist_id)

    return render_template('playlist.html', tracks=tracks, playlist_id=playlist_id)

@home_bp.route('/analisi/<playlist_id>')
@login_required
def analisi(playlist_id):
    charts = analyze_and_visualize(playlist_id)  
    return render_template('analisi.html', charts=charts, playlist_id=playlist_id)  
