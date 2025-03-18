from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from flask_login import login_required, current_user
from models import db, Playlist, UserPlaylist
from services.spotify_oauth import get_playlist_tracks, get_user_playlists, spotify_login as spotify_login_service, get_spotify_auth
from services.analisi import analyze_and_visualize

spotify_bp = Blueprint('spotify', __name__)

@spotify_bp.route('/spotify_login')
def spotify_login():
   
    return spotify_login_service()

@spotify_bp.route('/spotify_logout')
def spotify_logout():
   
    session.pop("token_info", None)
    flash('Logout da Spotify effettuato con successo.', 'success')
    return redirect(url_for('home.home'))

@spotify_bp.route('/saved_playlists')
@login_required
def saved_playlists():
    
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    user_playlists = UserPlaylist.query.filter_by(user_id=current_user.id).all()
    public_playlists = []
    for up in user_playlists:
        playlist = Playlist.query.get(up.playlist_id)
        if playlist:
            public_playlists.append({
                'id': playlist.id,
                'name': playlist.name,
                'owner': playlist.owner,
                'image': playlist.image
            })
        else:
            db.session.delete(up)
            db.session.commit()
    return render_template('saved_playlists.html', playlists=public_playlists)

@spotify_bp.route('/private_playlists')
@login_required
def private_playlists():
  
    if 'token_info' not in session:
        flash('Devi effettuare il login con Spotify per visualizzare le playlist private.', 'warning')
        return redirect(url_for('spotify.spotify_login')) 

    spotify_playlists = get_user_playlists()  
    return render_template('private_playlists.html', playlists=spotify_playlists)

@spotify_bp.route('/playlist/<playlist_id>')
def playlist(playlist_id):
    
    tracks = get_playlist_tracks(playlist_id)

    if not tracks:
        flash("Impossibile recuperare la playlist. Verifica il collegamento con Spotify.", "danger")
        return redirect(url_for('home.home'))

  
    charts = analyze_and_visualize(playlist_id)

  
    username = current_user.username if current_user.is_authenticated else "Ospite"

    return render_template('playlist.html', username=username, tracks=tracks, charts=charts)

@spotify_bp.route('/save_playlist', methods=['POST'])
@login_required
def save_playlist():
  
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    playlist_id = request.form.get('playlist_id')
    playlist_name = request.form.get('playlist_name')
    playlist_owner = request.form.get('playlist_owner')
    playlist_image = request.form.get('playlist_image')

    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        playlist = Playlist(id=playlist_id, name=playlist_name, owner=playlist_owner, image=playlist_image)
        db.session.add(playlist)
        db.session.commit()

    user_playlist = UserPlaylist.query.filter_by(user_id=current_user.id, playlist_id=playlist_id).first()
    if not user_playlist:
        user_playlist = UserPlaylist(user_id=current_user.id, playlist_id=playlist_id)
        db.session.add(user_playlist)
        db.session.commit()
        flash('Playlist salvata con successo!', 'success')
    else:
        flash('Hai già salvato questa playlist.', 'info')

    return redirect(url_for('home.home'))

@spotify_bp.route('/callback')
def spotify_callback():
   
    auth_manager = get_spotify_auth()
    code = request.args.get("code")
    if not code:
        return "Errore: Codice di autorizzazione mancante.", 400

    try:
        token_info = auth_manager.get_access_token(code)
        session["token_info"] = token_info
        return redirect(url_for('home.home'))
    except Exception as e:
        return f"Errore durante il callback di Spotify: {e}", 500