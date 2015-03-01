def logger(roles):
	def wrap(func):
		def wrapped(*args, **kwargs):
			print roles
			print "Arguments were: %s, %s" % (args, kwargs)
			return func(*args, **kwargs)
		return wrapped
	return wrap

@logger(roles=['admin'])
def foo(x, y=1):
	return x * y

foo(2, 3)