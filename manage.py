from flask.ext.script import Manager
from aniseasons import app, mongo
from werkzeug.security import generate_password_hash

manager = Manager(app)


@manager.command
def createuser(username, password):
    try:
        pass_hash = generate_password_hash(password)
        mongo.db.users.insert({'username': username, 'password': pass_hash})
    except e:
        return 'Could not create user {0}'.format(username)
    else:
        return '{0} was successfully created'.format(username)


@manager.command
def deleteuser(username):
    try:
        mongo.db.users.remove({'username': username})
    except:
        return 'Could not delete user {0}'.format(username)
    else:
        return '{0} was successfully deleted'.format(username)

if __name__ == '__main__':
    manager.run()
