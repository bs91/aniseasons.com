from flask import Blueprint, render_template

from aniseasons import mongo, GENRES, YEARS

mod = Blueprint('frontend', __name__)


@mod.route('/templates/<template_name>')
def templates(template_name):
    return render_template(template_name + ".html", genres=GENRES, years=YEARS)

@mod.route('/', defaults={'path': None})
@mod.route('/<path:path>')
def index(path):
    return render_template("base.html")
