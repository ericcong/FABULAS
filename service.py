from db import query, execute

def createUser(user):
	execute('insert into user (email, password) values (?, ?)', user['email'], user['password'])

def getUsers():
	return query('select email, password, id from user', ["email", "password", "id"])

def queryUsers(keywords):
	return query("select email, password, id from user where email like ?", ["email", "password", "id"], '%'+keywords.get('email')[0]+'%')

def getUser(id):
	return query("select email, password, id from user where id=?", ["email", "password", "id"], id)

def deleteUser(id):
	execute("delete from user where id=?", id)

def queryCOAs(legacy):
	# r = query("select PRE_LEGACY_CC, UNIT_CD || DIVISION_CD || ORGANIZATION_CD || LOCATION_CD || FUND_TYPE_CD || BUSINESS_CD || NATURAL_ACCT_CD || ACTIVITY_CD || INTRAUNIT_CD || FUTURE_CD from mapping where PRE_LEGACY_CC in (?)", ["legacy", "coa"], "'"+"','".join(legacy)+"'")
	r = query("select PRE_LEGACY_CC, UNIT_CD || DIVISION_CD || ORGANIZATION_CD || LOCATION_CD || FUND_TYPE_CD || BUSINESS_CD || NATURAL_ACCT_CD || ACTIVITY_CD || INTRAUNIT_CD || FUTURE_CD from mapping where PRE_LEGACY_CC in ("+"'"+"','".join(legacy)+"'"+")", ["legacy", "coa"])
	d = {}
	for e in r:
		d[e['legacy']]=e['coa']
	r = query("select FUND_SOURCE, LOCATION_CD || FUND_TYPE_CD || BUSINESS_CD, PRE_LEGACY_CC, UNIT_CD || DIVISION_CD || ORGANIZATION_CD || LOCATION_CD || FUND_TYPE_CD || BUSINESS_CD || NATURAL_ACCT_CD || ACTIVITY_CD || INTRAUNIT_CD || FUTURE_CD from mapping where FUND_SOURCE in ("+"'"+"','".join(legacy)+"'"+") order by FUND_SOURCE", ["legacy_fund_source", "coa_lfb", "legacy", "coa"])
	for e in r:
		d[e['legacy_fund_source']]=e['coa_lfb']
		d[e['legacy']]=e['coa']		
	return d