# system & 3rd party package
from flask import Flask, request, session, redirect, url_for, escape, abort
import json, urlparse, os.path, time, string, random

app = Flask(__name__)

# set app to debug mode to enable jsonp for all operations
app.debug = True

# put static files under static folder, it can be accessed without through flask route
@app.route('/courses')
def courses():
	return 'hello';
	# return '{"courseDescription":null,"expandedTitle":null,"subject":"001","credits":3,"subjectGroupNotes":null,"offeringUnitCode":"01","coreCodes":[],"preReqNotes":null,"offeringUnitTitle":null,"subjectNotes":null,"openSections":2,"sections":[{"honorPrograms":[],"crossListedSections":[],"sectionEligibility":null,"legendKey":null,"specialPermissionAddCode":null,"instructors":[],"minors":[],"sessionDates":null,"specialPermissionAddCodeDescription":null,"subtopic":null,"index":"07234","sessionDatePrintIndicator":"Y","examCode":"A","sectionNotes":null,"number":"01","specialPermissionDropCode":null,"stopPoint":25,"specialPermissionDropCodeDescription":null,"subtitle":null,"campusCode":"NB","openStatus":true,"printed":"N","meetingTimes":[{"campusAbbrev":"CAC","startTime":null,"meetingDay":null,"roomNumber":null,"meetingModeDesc":"PROJ-IND","baClassHours":"B","campusName":"COLLEGE AVENUE","pmCode":null,"campusLocation":"1","meetingModeCode":"19","buildingCode":null,"endTime":null}],"majors":[],"unitMajors":[],"comments":[]},{"honorPrograms":[],"crossListedSections":[],"sectionEligibility":null,"legendKey":null,"specialPermissionAddCode":null,"instructors":[],"minors":[],"sessionDates":null,"specialPermissionAddCodeDescription":null,"subtopic":null,"index":"07235","sessionDatePrintIndicator":"Y","examCode":"A","sectionNotes":null,"number":"02","specialPermissionDropCode":null,"stopPoint":25,"specialPermissionDropCodeDescription":null,"subtitle":null,"campusCode":"NB","openStatus":true,"printed":"N","meetingTimes":[{"campusAbbrev":"CAC","startTime":null,"meetingDay":null,"roomNumber":null,"meetingModeDesc":"PROJ-IND","baClassHours":"B","campusName":"COLLEGE AVENUE","pmCode":null,"campusLocation":"1","meetingModeCode":"19","buildingCode":null,"endTime":null}],"majors":[],"unitMajors":[],"comments":[]}],"title":"SSRA  COURSE","synopsisUrl":null,"courseNotes":null,"campusCode":"NB","unitNotes":null,"courseNumber":"001","supplementCode":"  "}]'

@app.before_request
def preProcess():
	return
	# if 'static' in request.url:
	# 	return
	# else:
	# 	if 'username' in session:
	# 		return
	# 	else:
	# 		abort(401)

@app.after_request
def postProcess(resp):
	if '.gz' in request.url:
		resp.headers["Content-Encoding"] = "gzip"
	# resp.headers["Access-Control-Allow-Origin"] = "*"
	# if 'json' in request.url:
	# 	resp.mimetype = "application/json"
	# else:
	# 	print resp.mimetype
	#wrap around data with callback function to support JSONP
	# if (JSONP and request.args.get(JSONP_CALLBACK, '')):
	# 	resp.set_data(request.args.get(JSONP_CALLBACK, '')+'('+ resp.get_data() +')')
	# 	resp.mimetype = "application/javascript"

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