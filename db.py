import sqlite3

# configuration
DATABASE = 'data.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


def connect_db():
    return sqlite3.connect(DATABASE)

def query(sql, attrs, *vars):
	db = None
	try:
		db = connect_db()
		print sql
		print vars
		cur = db.execute(sql, vars)
		length = len(attrs)
		entries = [{ attrs[i]:row[i] for i in range(length) } for row in cur.fetchall()]
		print entries
		return entries
	finally:
		db.close()

def execute(sql, *vars):
	db = None
	try:
		db = connect_db()
		cur = db.execute(sql, vars)
		db.commit()
	except:
		db.rollback()
	finally:
		db.close()