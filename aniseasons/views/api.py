from bson import json_util
from flask import Blueprint, request

from aniseasons import app, helpers, mongo

import os

mod = Blueprint('api', __name__, url_prefix='/api')

# GET /anime - Gets a list of all the anime
@mod.route('/anime/', methods=['GET'])
def retrieve_all_anime():
    return json_util.dumps(mongo.db.anime.find().sort([['_id', -1]]))


# GET /anime/name - Gets a specific anime
@mod.route('/anime/<name>', methods=['GET'])
def retrieve_anime_by_name(name):
    anime = mongo.db.anime.find_one_or_404(name)
    return json_util.dumps(anime)

# POST /anime - Creates a new anime
@mod.route('/anime/<name>', methods=['POST'])
def insert_anime(name):
    anime = {}

    if helpers.are_fields_valid(request):
        try:
            for key, value in request.form.iteritems():
                anime[key] = value

            anime['slug'] = helpers.slugify(anime['title'])

            filename = anime['slug'] + '.jpg'
            full_image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
            thumb_image_path = os.path.join(app.config['UPLOAD_PATH'], "thumb-" + filename)

            image = helpers.resize_image(request.files['file'], 600)
            image.save(full_image_path, 'JPEG', quality=95)
            thumb = helpers.resize_image(open(full_image_path), 194)
            thumb.save(thumb_image_path, 'JPEG', quality=95)

            anime['picture'] = filename
            anime['thumb'] = "thumb-" + filename

            mongo.db.anime.insert(anime)

            return "'{0}' has been added".format(anime['title'])
        except Exception as e:
            return str(e)
    else:
        return "All the required fields have not been completed"
        
    
# PUT /anime/name - updates a specific anime
# DELETE /anime/name - Deletes a specific anime
