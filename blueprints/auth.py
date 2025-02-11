from flask import Blueprint, redirect, request, session, url_for
from services.spotify_oauth import get_spotify_auth

auth_bp = Blueprint("auth", __name__)
sp_oauth = get_spotify_auth()

@auth_bp.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("home.home"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home.home"))
