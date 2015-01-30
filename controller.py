# system & 3rd party package
from flask import Flask, request
import json, urlparse
# user package
import service

app = Flask(__name__)

# set app to debug mode to enable jsonp for all operations
app.debug = True
# support for JSONP
JSONP = True
JSONP_CALLBACK = "callback"

# put static files under static folder, it can be accessed without through flask route

@app.route('/')
def hello_world():
    return 'Hello World!'

# JPSONP cross domain is ONLY support with HTTP GET method
@app.route('/users', methods=['GET'])
def getUsers():
	users = service.getUsers()
	return (json.dumps({"data": users, "message":"users retrieved"}))

# map url parts to variables
@app.route('/users/<id>', methods=['GET'])
def getUser(id):
	user = service.getUser(id)
	return (json.dumps({"data": user, "message":"user retrieved"}))

# special jsonp url for local test when app debug mode
@app.route('/users/delete/<int:id>', methods=['GET'])
# map url parts to variables
@app.route('/users/<int:id>', methods=['DELETE'])
def deleteUser(id):
	if ((request.method == 'DELETE') or app.debug):
		user = service.deleteUser(id)
		return (json.dumps({"message":"user deleted"}))

# HTTP GET method should NOT use msg body to communicate with server
@app.route('/users/query', methods=['GET'])
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
@app.route('/users/create', methods=['GET'])
# HTTP PUT, POST method use msg body to pass data either in form or json format
# Check request header Content-Type to find which data format
@app.route('/users', methods=['PUT', 'POST'])
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

@app.after_request
def postProcess(resp):
	resp.mimetype = "application/json"
	#wrap around data with callback function to support JSONP
	if (JSONP and request.args.get(JSONP_CALLBACK, '')):
		resp.set_data(request.args.get(JSONP_CALLBACK, '')+'('+ resp.get_data() +')')
		resp.mimetype = "application/javascript"
	return resp

if __name__ == '__main__':
    app.run()