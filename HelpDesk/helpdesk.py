from flask import Flask, render_template, request, redirect, session, g
from time import gmtime, strftime
import sqlite3

app = Flask(__name__)

problems = []
details = []

@app.before_request
def before_request():
    g.db = sqlite3.connect("problems.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/request')
def request_controller():
    return render_template('request.html')

@app.route('/submit-problem', methods = ['POST'])
def submit_problem():
    name = request.form['InputName']
    email = request.form['InputEmail']
    problem_title = request.form['InputTitle']
    description = request.form['InputMessage']
    usrfile = request.form['InputFile']
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    g.db.execute("INSERT INTO user_problems(name, email, title, description, file, time) VALUES (?, ?, ?, ?, ?, ?)", [name, email, problem_title, description, usrfile, current_time])
    g.db.commit()
    return redirect('/request')

@app.route('/problems')
def problems():
    problems = g.db.execute("SELECT * FROM user_problems").fetchall()
    return render_template('problems.html', problems = problems)

@app.route('/detail/<pid>')
def detail(pid):
    details = g.db.execute("SELECT * FROM user_problems WHERE pid = ?", [pid]).fetchall()
    return render_template('detail.html', details = details)

if __name__ == '__main__':
    app.secret_key = '\xb1\xa7@\xe5a^#b\x9d\x8f\xc6Dzz\xd6\x8f\x03A\xbf\x94\x99\x19`\x01'
    app.debug = True
    app.run()

