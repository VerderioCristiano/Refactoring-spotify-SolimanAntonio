from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from services.spotify_oauth import search_playlists, get_random_playlists

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
@login_required
def home():
    query = request.args.get("query")
    playlists = search_playlists(query) if query else get_random_playlists()
    return render_template('home.html', username=current_user.username, playlists=playlists)