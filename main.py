from flask import Flask, jsonify, url_for, render_template
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

app.secret_key = 'a_for_apple'
app.config['SERVER_NAME'] = 'localhost:5000'

oauth = OAuth(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    GOOGLE_CLIENT_ID = '672043905963-qk3ahr4eo924ng9oe8g1ljrf9khvis3h.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

    oauth.register(
        name = 'google',
        client_id=GOOGLE_CLIENT_ID,
        secret_key=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={'scope': 'openid email profile'}
    )

    redirect_uri = 'http://localhost:5000/google/auth'
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/google/auth')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    print('Google User:', user)
    return jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)
