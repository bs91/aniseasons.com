from flask import flash, session, redirect, url_for, render_template, request, Response
from werkzeug import secure_filename, check_password_hash
from PIL import Image
from bson import json_util
from jinja2 import evalcontextfilter, Markup, escape
from collections import OrderedDict

from app import app, mongo
from helpers import resize_image

import os
import re


@app.route('/')
def index():
    seasons = ['winter', 'spring', 'summer', 'fall']
    anime = OrderedDict()

    for season in seasons:
        anime[season] = mongo.db.anime.find({'season': season}).sort([['start', 1]])

    return render_template("index.html", seasons=anime)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # TODO: we need to roll our own @is_admin decorator
    if 'logged_in' not in session:
        if request.method == 'POST':
            user = mongo.db.users.find_one({'username': request.form['username']})
            if check_password_hash(user['password'], request.form['password']):
                session['logged_in'] = True
            else:
                flash('Incorrect credentials')

            return redirect(url_for('admin'))
        return render_template("add.html")

    return render_template("add.html", anime=mongo.db.anime.find().sort([['_id', -1]]))


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route('/manage/', methods=['POST'])
@app.route('/manage/<ObjectId:anime_id>', methods=['POST'])
def manage_anime(anime_id=None):
    anime_data = {}

    if request.files:
        filename = secure_filename(request.form['title'] + '.jpg') if request.form['title'] else secure_filename(request.files['file'].filename)
        # TODO: add exception handling when image resizing fails
        image = resize_image(request.files['file'], 600)
        image.save(os.path.join(app.config['UPLOAD_PATH'], filename), 'JPEG', quality=95)
        thumb = resize_image(open(os.path.join(app.config['UPLOAD_PATH'], filename)), 194)
        thumb.save(os.path.join(app.config['UPLOAD_PATH'], "thumb_" + filename), 'JPEG',  quality=95)

        anime_data['picture'] = filename
        anime_data['thumb'] = "thumb_" + filename

    for key, value in request.form.iteritems():
        value = re.sub('<[^<]+?>', '', value)
        anime_data[key] = value

    if anime_id is not None:
        mongo.db.anime.update({'_id': anime_id}, {'$set': anime_data})
        return "'{0}' has been updated".format(request.form['title'])
    else:
        mongo.db.anime.insert(anime_data)
        anime = mongo.db.anime.find_one({'title': request.form['title']})
        return "{0}".format(anime['_id'])


@app.route('/anime/', methods=['GET'])
def retrieve_animelist():
    return json_util.dumps(mongo.db.anime.find().sort([['_id', -1]]))


@app.route('/anime/<ObjectId:anime_id>', methods=['GET'])
def retrieve_anime(anime_id):
    anime = mongo.db.anime.find_one_or_404(anime_id)
    return json_util.dumps(anime)


@app.route('/delete/<ObjectId:anime_id>', methods=['POST'])
def delete_anime(anime_id):
    if 'logged_in' in session:
        anime = mongo.db.anime.find_one(anime_id)
        try:
            os.remove(os.path.join(app.config['UPLOAD_PATH'], anime['picture']))
            os.remove(os.path.join(app.config['UPLOAD_PATH'], anime['thumb']))
        except Exception as e:
            print e

        mongo.db.anime.remove({'_id': anime_id})

        return "Anime removed"
    else:
        return "You do not have permission to do that"

# flask glue
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2222, debug=True)
