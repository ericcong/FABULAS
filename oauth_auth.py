from flask import Flask, request, redirect, session, jsonify, url_for
import sqlite3
from flask_oauthlib.client import OAuth, OAuthException
from flask.ext.principal import Principal, Permission, identity_changed, Identity, identity_loaded

app = Flask(__name__)
Principal(app)
oauth = OAuth(app)


app.debug = True    # TODO: in production, change this to 'False'
app.secret_key = 'super secret key'     # TODO: change this!!!


# TODO: Define Permission tags here.
logged_in_permission = Permission(('logged in'))
role_admin_permission = Permission(('role', 'admin'))


# TODO: change this
consumer_key = ''
consumer_secret = ''


google = oauth.remote_app(
    'google',
    consumer_key = consumer_key,
    consumer_secret = consumer_secret,
    request_token_params = {
        'scope': 'https://www.googleapis.com/auth/userinfo.email'
    },
    base_url = 'https://www.googleapis.com/oauth2/v1/',
    request_token_url = None,
    access_token_method = 'POST',
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
)
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


# TODO: Authentication
@app.route('/login')
def login():
    return google.authorize(callback = url_for('authorized', _external = True))

@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if isinstance(resp, OAuthException):    
        return 'Access denied: %s' % resp.message
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    user_id = google.get('userinfo').data['id']
    identity_changed.send(app, identity = Identity(user_id, 'google'))
    return redirect('/')


# TODO: Authorization
@identity_loaded.connect_via(app)
def get_user_info(sender, identity):
    if hasattr(identity, 'id') and identity.id != None:
        identity.provides.add(('logged in'))
        identity.provides.add(('user', 'google', identity.id))
    role_database = sqlite3.connect('roles.db')
    cursor = role_database.cursor()
    cursor.execute("SELECT role FROM roles WHERE user_id = '{0}' AND auth_type = '{1}'".format(identity.id, identity.auth_type))
    for record in cursor.fetchall():
        identity.provides.add(('role', record[0]))


# TODO controllers protected by permissions
@app.route('/')
def index():
    if 'google_token' in session:
        return jsonify({'status': 'OK'})
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()
    identity_changed.send(app, identity = Identity(None))
    return jsonify({'controller': 'logout', 'status': 'OK'})


@app.route('/admin')
@role_admin_permission.require(403)
def admin():
    return jsonify({'controller': 'admin', 'status': 'OK'})


@app.route('/test')
@logged_in_permission.require(403)
def logged_in():
    return 'logged in'


# TODO error handlers
@app.errorhandler(403)
def page_not_found(e):
    return jsonify({'status': 403, 'message': 'unauthorized'})


if __name__ == '__main__':
    app.run()