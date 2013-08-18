from flask import Blueprint, render_template

from aniseasons import mongo, GENRES, YEARS

mod = Blueprint('frontend', __name__)


@mod.route('/')
def index():
    return render_template("index.html", genres=GENRES, years=YEARS)

@mod.route('/admin')
def admin():
    return render_template("admin.html", genres=GENRES, years=YEARS)
