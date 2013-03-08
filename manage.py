from flask.ext.script import Manager
from aniseasons import app, mongo
from werkzeug.security import generate_password_hash

manager = Manager(app)

@manager.command
def createuser(username, password):
    pass_hash = generate_password_hash(password)
    mongo.db.users.insert({'username': username, 'password': pass_hash})

if __name__ == '__main__':
    manager.run()
