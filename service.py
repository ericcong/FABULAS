from db import query, execute

def createUser(user):
	execute('insert into user (email, password) values (?, ?)', user['email'], user['password'])

def getUsers():
	return query('select email, password, id from user', ["email", "password", "id"]);

def queryUsers(keywords):
	return query("select email, password, id from user where email like ?", ["email", "password", "id"], '%'+keywords.get('email')[0]+'%');

def getUser(id):
	return query('select email, password, id from user where id=?', ["email", "password", "id"], id);

def deleteUser(id):
	execute('delete from user where id=?', id)
