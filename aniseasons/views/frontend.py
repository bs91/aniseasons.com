from flask import Blueprint, render_template

from aniseasons import mongo

mod = Blueprint('frontend', __name__)


@mod.route('/')
def index():
    years = []
    genres = []

    anime = mongo.db.anime.find()

    # make this into a funky list comprehension when less brain-dead
    for entry in anime:
        for genre in entry['genre']:
            if genre not in genres:
                genres.append(genre)

        if entry['year'] not in years and entry['year']:
            years.append(entry['year'])

    return render_template("index.html", years=years, genres=genres)
