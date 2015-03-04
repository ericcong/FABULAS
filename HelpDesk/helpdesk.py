from flask import Flask, render_template, request, redirect, session, g
import sqlite3

app = Flask(__name__)

email_addresses = []

@app.before_request
def before_request():
    g.db = sqlite3.connect("emails.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    g.db.execute("INSERT INTO email_addresses VALUES (?)", [email])
    g.db.commit()
    return redirect('/')

@app.route('/unregister')
def unregister():
    # Make sure they've already registered an email address
    if 'email' not in session:
        return "You haven't submitted an email!"
    email = session['email']
    # Make sure the email was already in the email list
    if email not in email_addresses:
        return "That address is not in our list"
    email_addresses.remove(email)
    del session['email'] # Remove email from the session dictionary
    return "We have removed " + email + " from the list"

@app.route('/emails.html')
def emails():
    email_addresses = g.db.execute("SELECT * FROM email_addresses").fetchall()
    return render_template('emails.html', email_addresses = email_addresses)

if __name__ == '__main__':
    app.secret_key = '\xb1\xa7@\xe5a^#b\x9d\x8f\xc6Dzz\xd6\x8f\x03A\xbf\x94\x99\x19`\x01'
    app.run()

