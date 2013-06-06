from bson import json_util
from flask import Blueprint, request
from flask.views import MethodView

from aniseasons import app, helpers, mongo

import os


class AnimeAPI(MethodView):

    def get(self, slug):
        if name is None:
            # GET /anime - Gets a list of all the anime
            return json_util.dumps(mongo.db.anime.find().sort([['_id', -1]]))
        else:
            # GET /anime/<name> - Gets a specific anime
            anime = mongo.db.anime.find_one_or_404({'slug': slug})
            return json_util.dumps(anime)


    def post(self):
        # POST /anime - Creates a new anime
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


def delete(self, slug):
        # DELETE /anime/name - Deletes a specific anime
        pass


def put(self, slug):
        # PUT /anime/name - updates a specific anime
        pass


mod = Blueprint('api', __name__, url_prefix='/api')
anime_view = AnimeAPI.as_view('anime_api')
mod.add_url_rule('/anime/', defaults={'name': None}, view_func=anime_view, methods=['GET'])
mod.add_url_rule('/anime/', view_func=anime_view, methods=['POST'])
mod.add_url_rule('/anime/<name>', view_func=anime_view, methods=['GET', 'PUT', 'DELETE'])
