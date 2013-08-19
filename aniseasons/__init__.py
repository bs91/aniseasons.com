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

def get_genre_and_years():
    # weird application context error when using `mongo`
    from pymongo import MongoClient

    client = MongoClient('localhost', 27017)
    db = client[app.config['MONGO_DBNAME']]

    anime = db.anime.find()

    genres = []
    years = []

    # make this into a funky list comprehension when less brain-dead
    for entry in anime:
        if 'genre' in entry.keys():
            for genre in entry['genre']:
                if genre not in genres and genre != '':
                    genres.append(genre)

        if entry['year'] not in years and entry['year']:
            years.append(entry['year'])

    return (tuple(genres), tuple(years))

GENRES, YEARS = get_genre_and_years()

from aniseasons.views import frontend
from aniseasons.views import api

app.register_blueprint(frontend.mod)
app.register_blueprint(api.mod)

from aniseasons import filters

app.jinja_env.filters['nl2br'] = filters.nl2br
