import json, urllib2, os, commands, time, datetime

json_data=open('units.json')
data = json.load(json_data)
json_data.close()
data = data['units']
units = {}
for k in data:
	units[k['code']] = k['description']
year = '2015'
term = '1'
courses = []
st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
print st + " - start loading courses."
for k in units:
	url = 'https://test-sis.rutgers.edu/soc/schoolCourses.json?year='+year+'&term='+term+'&school='+k
	response = urllib2.urlopen(url)
	html = response.read()
	j = json.loads(html)
	courses = courses + j
st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
print st + " - loaded " + str(len(courses)) + " courses."
with open('new-20151courses.json', 'w') as outfile:
    json.dump(courses, outfile)

result = commands.getstatusoutput('gzip new-20151courses.json')
if (result[0] == 0):
	os.rename('new-20151courses.json.gz', '20151courses.json.gz')
	print st + " - course gzip file updated."