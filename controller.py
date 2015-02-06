# system & 3rd party package
from flask import Flask, request, session, redirect, url_for, escape, abort
import json, urlparse, os.path, time, string, random

from werkzeug import secure_filename

# user package
import service

app = Flask(__name__)

# set app to debug mode to enable jsonp for all operations
app.debug = True
# set the secret key.  keep this really secret:
app.secret_key = 'B0Wrc3d/3yX R~XHD!jxN]kWX/,?wT'

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'upload/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mov'])
# max file size 16M
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# support for JSONP
JSONP = True
JSONP_CALLBACK = "callback"

# put static files under static folder, it can be accessed without through flask route

@app.route('/static')
def index():
	return 'Hello World'

@app.route('/whoami')
def whoami():
	return 'Logged in as %s' % escape(session['username'])

# JPSONP cross domain is ONLY support with HTTP GET method
@app.route('/json/users', methods=['GET', 'POST'])
def getUsers():
	users = service.getUsers()
	return (json.dumps({"data": users, "message":"users retrieved"}))

# map url parts to variables
@app.route('/json/users/<id>', methods=['GET', 'POST'])
def getUser(id):
	user = service.getUser(id)
	return (json.dumps({"data": user, "message":"user retrieved"}))

# special jsonp url for local test when app debug mode
@app.route('/json/users/delete/<int:id>', methods=['GET', 'POST'])
# map url parts to variables
@app.route('/json/users/<int:id>', methods=['DELETE'])
def deleteUser(id):
	if ((request.method == 'DELETE') or app.debug):
		user = service.deleteUser(id)
		return (json.dumps({"message":"user deleted"}))

# HTTP GET method should NOT use msg body to communicate with server
@app.route('/json/users/query', methods=['GET, POST'])
def queryUsers():
	# get whole query string or individual query param
	#print request.query_string
	#print request.args.get(url_param_name, default_value)

	# convert whole query_string to json
	#print urlparse.parse_qs(request.query_string)
	# url param may have array as value id=1&id=2&id=3 {"id": ["1", "2, "3]}
	query = urlparse.parse_qs(request.query_string)
	print query
	#print urlparse.parse_qs(request.query_string)['id'][0]

	users = service.queryUsers(query)
	return (json.dumps({"data": users, "message":"Users Retrieved."}))

# special jsonp for local prototype when app debug mode
@app.route('/static/json/users/create', methods=['GET', 'POST'])
# HTTP PUT, POST method use msg body to pass data either in form or json format
# Check request header Content-Type to find which data format
def createUser():
	# request header Content-Type: application/json with body {"email":"jane@me.com", "password":"jane"} 
	# request header Content-Type: multipart/form-data with binary body to support file upload
	# request header Content-Type: application/x-www-form-urlencoded with body email=jane@me.com&password=jane
	#print request.mimetype		
	# get form data
	#print request.form.get("email")

	# get json data
	u = request.get_json()
	# if not json, get form data and convert it to json
	if not u:
		u = request.form.to_dict()
	# if not form, get query string and convert it to json
	if (app.debug and (not u)):
		params = urlparse.parse_qs(request.query_string)
		for param in params:
			u[param] = params[param][0] 
	print u

	service.createUser(u)
	return (json.dumps({"message":"user created"}))


@app.route('/upload', methods=['POST'])
def upload():
	result = []
	if request.method == 'POST':
		# Get the name of the uploaded file
		fileset = request.files.getlist('files')
		for file in fileset:
			# Make the filename safe, remove unsupported chars
			filename = secure_filename(file.filename)
			filename = filename.lower()
			if file and allowed_file(filename):
				filename = id_generator(8) + '.' + filename
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				# {"files": [
				#   {
				#     "name": "picture1.jpg",
				#     "size": 902604,
				#     "url": "http:\/\/example.org\/files\/picture1.jpg",
				#     "thumbnailUrl": "http:\/\/example.org\/files\/thumbnail\/picture1.jpg",
				#     "deleteUrl": "http:\/\/example.org\/files\/picture1.jpg",
				#     "deleteType": "DELETE"
				#   },
				#   {
				#     "name": "picture2.jpg",
				#     "size": 841946,
				#     "url": "http:\/\/example.org\/files\/picture2.jpg",
				#     "thumbnailUrl": "http:\/\/example.org\/files\/thumbnail\/picture2.jpg",
				#     "deleteUrl": "http:\/\/example.org\/files\/picture2.jpg",
				#     "deleteType": "DELETE"
				#   }
				# ]}
				result.append({"name": filename})
	return (json.dumps({"files": result, "message":"Files Uploaded."}))

@app.route('/static/login', methods=['GET', 'POST'])
def login():
	# get json data
	u = request.get_json()
	# if not json, get form data and convert it to json
	if not u:
		u = request.form.to_dict()
	# if not form, get query string and convert it to json
	if (app.debug and (not u)):
		params = urlparse.parse_qs(request.query_string)
		for param in params:
			u[param] = params[param][0] 
	print u

	# check username password
	session['username'] = u['username']
	return (json.dumps({"message":"Login Success.", "data":{"name":"fei"}}))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return (json.dumps({"message":"Logout Success."}))

@app.before_request
def preProcess():
	if 'static' in request.url:
		return
	else:
		if 'username' in session:
			return
		else:
			abort(401)

@app.after_request
def postProcess(resp):
	if 'json' in request.url:
		resp.mimetype = "application/json"
	else:
		print resp.mimetype
	#wrap around data with callback function to support JSONP
	if (JSONP and request.args.get(JSONP_CALLBACK, '')):
		resp.set_data(request.args.get(JSONP_CALLBACK, '')+'('+ resp.get_data() +')')
		resp.mimetype = "application/javascript"

	# if (app.debug):
	# 	resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	# 	resp.headers["Pragma"] = "no-cache"
	# 	resp.headers["Expires"] = "0"
	
	return resp

# generate random id
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    app.run(debug=True)