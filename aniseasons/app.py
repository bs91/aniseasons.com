from flask import Flask
from flask.ext.pymongo import PyMongo

import os

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('ANIMELIST_SETTINGS', silent=True)
app.secret_key = '}\xa8\xcd!\xcf\x00\\\xe7b\xec\x8a\\\xfdf\xd3J #\x880HUH\xb7'
app.config['DEBUG'] = True
app.config['MONGO_DBNAME'] = 'aniseasons-dev'
app.config['PROJECT_PATH'] = os.path.realpath(os.path.dirname(__file__))
app.config['MEDIA_PATH'] = os.path.join(app.config['PROJECT_PATH'], 'media')
app.config['UPLOAD_PATH'] = os.path.join(app.config['PROJECT_PATH'], 'media/imgs/')
app.config['STATIC_PATH'] = os.path.join(app.config['PROJECT_PATH'], 'static')

mongo = PyMongo(app)

if not os.path.exists(app.config['UPLOAD_PATH']):
    os.makedirs(app.config['UPLOAD_PATH'])
    os.chmod(app.config['MEDIA_PATH'], 0775)
    os.chmod(app.config['UPLOAD_PATH'], 0775)

if app.config['DEBUG']:
    from werkzeug import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/media': app.config['MEDIA_PATH'],
        '/static': app.config['STATIC_PATH'],
    })
