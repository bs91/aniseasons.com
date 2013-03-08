from flask.ext.script import Manager
from aniseasons import app, mongo
from werkzeug.security import generate_password_hash

manager = Manager(app)

@manager.command
def createuser(username, password):
    try:
        pass_hash = generate_password_hash(password)
        mongo.db.users.insert({'username': username, 'password': pass_hash})
    except:
        print 'Could not create user {0}'.format(username)
    else:
        print '{0} was successfully created'.format(username)

if __name__ == '__main__':
    manager.run()
