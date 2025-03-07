import os
from flask import Blueprint, session, redirect, url_for, jsonify
from app.extensions import oauth, db
import secrets

from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    # Configure Google OAuth
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

    session['nonce'] = secrets.token_urlsafe(16)
    redirect_uri = url_for('auth.google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])


@auth_bp.route('/google/auth')

def google_auth():

    token = oauth.google.authorize_access_token()
    # print(f"Token Payload: {token}")
    #
    # print(f"Received Url : {request.url}")
    # print(f"Received Args : {request.args}")

    nonce = session.get('nonce')
    if not nonce:
        return jsonify({'error': 'Nonce is missing or invalid'}), 400

    try:
        user = oauth.google.parse_id_token(token, nonce=nonce)
    except Exception as e:
        return jsonify({'error': f'Invalid token: {str(e)}'}), 400

    email = user.get('email')
    name = user.get('name')
    picture = user.get('picture')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user is None:
        new_user = User(email=email, name=name, picture=picture)
        db.session.add(new_user)
        db.session.commit()


    # print('Google User:', user)
    # print(f"Stored Nonce: {nonce}")

    return jsonify(user)