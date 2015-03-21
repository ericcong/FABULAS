import json, urllib2, os, commands, time, datetime, sys

json_data=open('units.json')
data = json.load(json_data)
json_data.close()
data = data['units']
units = {}
for k in data:
	units[k['code']] = k['description']
year = argv[1]
term = argv[2]
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
filename = ""+term+""+year+'courses.json'
newfilename = "new-"+filename
with open(newfilename, 'w') as outfile:
    json.dump(courses, outfile)

result = commands.getstatusoutput('gzip '+newfilename)
if (result[0] == 0):
	os.rename(newfilename+'.gz', filename+'.gz')
	print st + " - "+filename+".gz updated."