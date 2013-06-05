from flask import Flask
from flask.ext.pymongo import PyMongo

from aniseasons.settings import Settings

import os


app = Flask(__name__)
app.config.from_object(Settings)

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

from aniseasons import filters

app.jinja_env.filters['nl2br'] = filters.nl2br
