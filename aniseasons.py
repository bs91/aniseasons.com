from flask import Flask, flash, session, redirect, url_for, render_template, request, Response
from flask.ext.pymongo import PyMongo
from werkzeug import secure_filename, check_password_hash
from PIL import Image
from bson import json_util
from jinja2 import evalcontextfilter, Markup, escape
from collections import OrderedDict

import os
import re

# flask app settings
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('ANIMELIST_SETTINGS', silent=True)
app.secret_key = '}\xa8\xcd!\xcf\x00\\\xe7b\xec\x8a\\\xfdf\xd3J #\x880HUH\xb7'
app.config['DEBUG'] = True
app.config['PROJECT_PATH'] = os.path.realpath(os.path.dirname(__file__))
app.config['MEDIA_PATH'] = os.path.join(app.config['PROJECT_PATH'], 'media')
app.config['UPLOAD_PATH'] = os.path.join(app.config['PROJECT_PATH'], 'media/imgs/')
app.config['STATIC_PATH'] = os.path.join(app.config['PROJECT_PATH'], 'static')

if not os.path.exists(app.config['UPLOAD_PATH']):
    os.makedirs(app.config['UPLOAD_PATH'])

if app.config['DEBUG']:
    from werkzeug import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/media': app.config['MEDIA_PATH'],
        '/static': app.config['STATIC_PATH'],
    })

# mongo connection initialization
mongo = PyMongo(app)

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

# helper method for resizing images to proper size
def resize_image(pic):
    im = Image.open(pic)
    dimensions = im.size
    max_width = 428

    width_percent = (max_width / float(dimensions[0]))
    new_height = int((float(dimensions[1]) * float(width_percent)))

    return im.resize((max_width, new_height), Image.ANTIALIAS)


@app.route('/')
def index():
    seasons = ['winter', 'spring', 'summer', 'fall']
    anime = OrderedDict()

    for season in seasons:
        anime[season] = mongo.db.anime.find({'season': season})

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
        image = resize_image(request.files['file'])
        image.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        anime_data['picture'] = filename
        anime_data['picture-width'] = image.size[0]
        anime_data['picture-height'] = image.size[1]

    for key, value in request.form.iteritems():
        value = re.sub('<[^<]+?>', '', value)
        anime_data[key] = value

    if anime_data['start']:
        anime_data['year'] = anime_data['start'].split('/')[2]

    if anime_id is not None:
        mongo.db.anime.update({'_id': anime_id}, {'$set': anime_data})
        return "'{0}' has been updated".format(request.form['title'])
    else:
        mongo.db.anime.insert(anime_data)
        return "'{0}' has been added to the database".format(request.form['title'])


@app.route('/anime/', methods=['GET'])
def retrieve_animelist():
    return json_util.dumps(mongo.db.anime.find())


@app.route('/anime/<ObjectId:anime_id>', methods=['GET'])
def retrieve_anime(anime_id):
    anime = mongo.db.anime.find_one_or_404(anime_id)
    return json_util.dumps(anime)


@app.route('/delete/<ObjectId:anime_id>', methods=['POST'])
def delete_anime(anime_id):
    anime = mongo.db.anime.find_one(anime_id)
    os.remove(os.path.join(app.config['UPLOAD_PATH'], anime['picture']))
    mongo.db.anime.remove({'_id': anime_id})

    return "Anime removed"

# flask glue
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2222, debug=True)
