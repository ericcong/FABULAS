from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import requests

app = Flask(__name__)
app.debug = True
app.secret_key = 'super secret key'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key = '533897933561-av8uoahfptbgboh22rimfsvv7i9f9829.apps.googleusercontent.com',
    consumer_secret = 'wif9PC9DEWkvnis7KGtkL-24',
    request_token_params = {
        'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/drive'
    },
    base_url = 'https://www.googleapis.com/oauth2/v1/',
    request_token_url = None,
    access_token_method = 'POST',
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return google.authorize(callback = url_for('authorized', _external = True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return jsonify({"data": me.data})

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_name = file.filename
    content_type = file.content_type
    content = file.read()

    meta_data = "{ \"title\": \"%s\"}" % file_name

    meta_headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'Content-Length': str(len(meta_data)),
        'Authorization': 'Bearer %s' % session['google_token'][0],
        'X-Upload-Content-Type': content_type,
        'X-Upload-Content-Length': str(len(content))
    }

    upload_session_response = requests.post('https://www.googleapis.com/upload/drive/v2/files?uploadType=resumable', headers = meta_headers, data = meta_data)
    upload_session_url = upload_session_response.headers['Location']

    headers = {
        'Authorization': 'Bearer %s' % session['google_token'][0],
        'Content-Type': content_type,
        'Content-Length': str(len(content))
    }

    upload_response = requests.put(upload_session_url, headers = headers, data = content)

    return str(upload_response.text)

if __name__ == '__main__':
    app.run()