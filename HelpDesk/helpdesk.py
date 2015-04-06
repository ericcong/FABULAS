from flask import Flask, render_template, request, redirect, session, url_for, g, send_from_directory
from time import gmtime, strftime
from werkzeug import secure_filename
import sqlite3
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

problems = []
details = []

@app.before_request
def before_request():
    g.db = sqlite3.connect("problems.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

#Login/SignUp Page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        return "the method is post"
    else:
        return render_template('login.html')

#SignUp action
@app.route('/signup', methods = ['POST'])
def signup():
    

@app.route('/request')
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
def problems():
    problems = g.db.execute("SELECT * FROM user_problems").fetchall()
    return render_template('problems.html', problems = problems)

#The Problem detail after clicked on row
@app.route('/detail/<pid>')
def detail(pid):
    details = g.db.execute("SELECT * FROM user_problems WHERE pid = ?", [pid]).fetchall()
    return render_template('detail.html', details = details)

if __name__ == '__main__':
    app.secret_key = '\xb1\xa7@\xe5a^#b\x9d\x8f\xc6Dzz\xd6\x8f\x03A\xbf\x94\x99\x19`\x01'
    app.debug = True
    app.run()

