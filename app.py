from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import paho.mqtt.publish as publish
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'FKLADSJFKADS'
CORS(app, supports_credentials=True)

oauth = OAuth(app)  # initialising the OAuth obj

github = oauth.register(
    name='github',
    client_id='Ov23liIdwVA93kxERkha',
    client_secret='f095db1071ad4331150e6a936d6a4fd77022efb5',
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'user:email'},
)


@app.route('/')
def hello_world():
    if 'user_name' not in session:
        return f'Hello, stranger'
    else:
        return f'Hello, {session["user_name"]}'


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = github.authorize_access_token()
    resp = oauth.github.get('https://api.github.com/user')
    resp.raise_for_status()
    profile = resp.json()
    session['user_name'] = profile['login']
    return redirect('/')
