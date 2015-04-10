# How to use this template?
# Find and do all the TODO's in this template.

from flask import Flask, request, session
import sqlite3

from flask.ext.principal import Principal, Permission, identity_changed, Identity, identity_loaded

app = Flask(__name__)
Principal(app)

app.debug = True    # TODO: in production, change this to 'False'

app.secret_key = 'super secret key'     # TODO: change this!!!

# 1. Permission tags:
#
# A Permission tag is essentially tuples for access control.
# Every Permission tag can have one or more tuples, every user can have several Permission tags, as well as every URL.
#
# If a Permission tag has more than one tuples, then it will be used as an "OR" gate, for example:
# If a URL has the tag (('role', 'admin'), ('logged in')),
# then any user with either ('role', 'admin') or ('logged in') tag can use this URL
# Permission tags can union and difference other tags, they can also be reversed.
#
# Some examples:
#
# logged_in_permission = Permission(('logged in'))
# id_1_permission = Permission(('id', 1))
# role_admin_permission = Permission(('role', 'admin'))
# role_admin_or_editor = Permission(('role', 'admin'), ('role', 'editor'))
# role_admin_or_id_1_permission = role_admin_permission.union(id_1_permission)
#
# In order to make an "AND" gate, we can use multiple access control decorators for a URL, for example:
#
#   @app.route('/admin')
#   @logged_in_permission.require(403)
#   @admin_permission.require(403)
#   def admin():
#       return 'admin'
#
# will only allow the users that have both ('logged in') and ('role', 'admin') tag

# TODO: Define Permission tags here.


# 2. Log in
# 
# Here we get the user's ID and cast "identity_changed" event
# Provide the user's ID and authentication type when casting the event
# The authentication phase can be implemented in any ways, such as database, CAS, and OAUTH
# as long as we can get the user ID and designate the authentication type.

@app.route('/login', methods=['GET'])
def login():

    # Here is an example of how to get the user ID and authentication type:
    #
    # auth_type = "database"
    # username = request.args['username']
    # password = request.args['password']
    # login_database = sqlite3.connect('users.sqlite3')
    # cursor = login_database.cursor()
    # cursor.execute("SELECT * FROM user WHERE username = '{0}' AND password = '{1}'".format(username, password))
    # records = cursor.fetchall()
    # if len(records) == 0:
    #     return 'Could not verify your access level for that URL', 401
    # else:
    #     user_id = records[0][0]

    # TODO: get user_id and auth_type

    identity_changed.send(app, identity = Identity(user_id, auth_type))

    # Then redirect or render something, for example:
    #
    # return 'Logged in'

    # TODO: redirect or render something


# 3. Get user information
#
# Here we will fetch the user's information and most important, the user's Permission tags based on the user ID and authentication type
# after successfully logged in.
# It's worth noticing that the user's information can be fetched from places other than the login service.
# We can fetch user ID and authentication type by subscribing to "identity_loaded" event

@identity_loaded.connect_via(app)
def get_user_info(sender, identity):

    # Here we find and add the user's Permission tags, for example:
    #
    # identity.provides.add(('logged in'))
    # if hasattr(identity, 'id'):
    #     identity.provides.add(('id', identity.id))
    # role_database = sqlite3.connect('roles.sqlite3')
    # cursor = role_database.cursor()
    # cursor.execute("SELECT role FROM roles WHERE user_id = '{0}'".format(identity.id))
    # for record in cursor.fetchall():
    #     identity.provides.add(('role', record[0]))

    # TODO: add user's Permission tags

    # We can also add other user information here, for example:
    #
    # session['identity.gender'] = 'male'

    # TODO: add other user information


# 4. Log out
#
# Log out requires the erasing of all identity related session data and casting an "identity_changed" event with an empty identity.
@app.route('/logout')
def logout():
    session.clear()
    identity_changed.send(app, identity = Identity(None))

    # After clearing the session and casting the identity_changed event, we can do some follow-up operations, for example:
    #
    # return 'Logged out'

    # TODO: some follow-ups after loggin out


# 5. Routes with access control
#
# Here we enforce the access control by adding permission decorators after the URL.
# We can add multiple permission decorators to make an "AND" gate.
# In the decorators, we can also designate HTTP error codes when the user doesn't have the tags.
#
# Example:
#
# @app.route('/admin')
# @role_admin_permission.require(403)
# @id_1_permission.require(403)
# def admin():
#     return 'hello'

# TODO: add routes, as well as permission decorators.


# 6. Error handling
# 
# Here we handle HTTP errors, for example:
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return "404 error"

# TODO: add error handlers


if __name__ == '__main__':
    app.run()
