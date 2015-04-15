from flask import Flask, render_template, request, redirect, session, url_for, g, send_from_directory
from time import gmtime, strftime
from werkzeug import secure_filename
from flask.ext.principal import Principal, Permission, identity_changed, Identity, identity_loaded
import sqlite3
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
Principal(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

problems = []
details = []

# Define Permission tags here.
logged_in_permission = Permission(('logged in'))
role_admin_permission = Permission(('role', 'admin'))
role_client_permission = Permission(('role', 'client'))

@app.before_request
def before_request():
    g.db = sqlite3.connect("mydb.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


#Login/SignUp Page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        #return "the method is post"
        #auth_type = ""
        username = request.form['InputUserName']
        password = request.form['InputPassword']
        records = g.db.execute("SELECT * FROM users WHERE username = ?", [username]).fetchall()
        if records:
            user_id = records[0][0]
        else:
            return "!!!username not exists!!!"

        identity_changed.send(app, identity = Identity(user_id))
        return "!!!You have successfully logged in!!!" + str(user_id)
    else:
        return render_template('login.html')


# Get User Information
@identity_loaded.connect_via(app)
def get_user_info(sender, identity):
    identity.provides.add(('logged in'))
    #if hasattr(identity, 'id'):
    #    identity.provides.add(('id', identity.id))
    database = sqlite3.connect("mydb.db")
    records = database.execute("SELECT role FROM users WHERE uid = ?", [identity.id]).fetchall()
    for record in records:
        identity.provides.add(('role', record[0]))


#SignUp action
@app.route('/signup', methods = ['POST'])
def signup():
    username = request.form['InputUserName']
    email = request.form['InputEmail']
    password = request.form['InputPassword']

    # TODO: get input role
    checked = request.form.get('InputRole')
    if checked:
        role = 'admin'
    else:
        role = 'client'

    records = g.db.execute("SELECT * FROM users WHERE username = ?", [username]).fetchall()
    if records:
        return "!!!username already exists!!!"
    else:
        g.db.execute("INSERT INTO users(username, email, password, role) VALUES(?, ?, ?, ?)", [username, email, password, role])
        g.db.commit()
        return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()
    identity_changed.send(app, identity = Identity(None))
    return "You have successfully logged out"


@app.route('/request')
@role_client_permission.require(403)
def request_controller():
    return render_template('request.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#Submit the problem request form
@app.route('/submit-problem', methods = ['POST'])
def submit_problem():
    name = request.form['InputName']
    email = request.form['InputEmail']
    problem_title = request.form['InputTitle']
    description = request.form['InputMessage']
    #file = request.form['InputFile']
    file = request.files['InputFile']
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    g.db.execute("INSERT INTO user_problems(name, email, title, description, file, time) \
            VALUES (?, ?, ?, ?, ?, ?)", [name, email, problem_title, description, file.filename, current_time])
    g.db.commit()
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect('/request')


#Display the uploaded file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


#The Problems List Page
@app.route('/problems')
@role_admin_permission.require(403)
def problems():
    problems = g.db.execute("SELECT * FROM user_problems").fetchall()
    return render_template('problems.html', problems = problems)


#The Problem detail after clicked on row
@app.route('/detail/<pid>')
@role_admin_permission.require(403)
def detail(pid):
    details = g.db.execute("SELECT * FROM user_problems WHERE pid = ?", [pid]).fetchall()
    return render_template('detail.html', details = details)

if __name__ == '__main__':
    app.secret_key = '\xb1\xa7@\xe5a^#b\x9d\x8f\xc6Dzz\xd6\x8f\x03A\xbf\x94\x99\x19`\x01'
    app.debug = True
    app.run()

