import os
import secrets
from authlib.integrations.flask_client import OAuth
from flask import Flask, jsonify, render_template, request
from flask import session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-fallback-key')
app.config['SERVER_NAME'] = 'localhost:5000'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

oauth = OAuth(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    picture = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

    oauth.register(
        name = 'google',
        client_id=os.environ.get('GOOGLE_CLIENT_ID'),
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url=CONF_URL,
        client_kwargs={'scope': 'openid email profile https://www.googleapis.com/auth/userinfo.email'}
    )

    session['nonce'] = secrets.token_urlsafe(16)

    redirect_uri = 'http://localhost:5000/google/auth'
    return oauth.google.authorize_redirect(
        redirect_uri,
        nonce=session['nonce']
    )


@app.route('/google/auth')
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


@app.route('/get_users')
def get_users():
    users = User.query.all()
    return jsonify([{'email' : user.email, 'name' : user.name, 'picture' : user.picture} for user in users])

if __name__ == '__main__':
    app.run(debug=True)
