# system & 3rd party package
from flask import Flask, request, session, redirect, url_for, escape, abort
import json, urlparse, os.path, time, string, random

app = Flask(__name__)

# set app to debug mode to enable jsonp for all operations
app.debug = True

# put static files under static folder, it can be accessed without through flask route
@app.before_request
def preProcess():
	return

@app.after_request
def postProcess(resp):
	if '.gz' in request.url:
		resp.headers["Content-Encoding"] = "gzip"
	
	return resp

if __name__ == '__main__':
    app.run(debug=True)