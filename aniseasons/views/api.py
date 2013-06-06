from bson import json_util
from flask import Blueprint, request
from flask.views import MethodView

from aniseasons import app, helpers, mongo

import os


class AnimeAPI(MethodView):

    def get(self, slug):
        if slug is None:
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

                saved_files = helpers.save_image_and_thumbnail(anime['slug'], request.files['file'], app.config['UPLOAD_PATH'])

                anime['picture'] = saved_files[0]
                anime['thumb'] = saved_files[1]

                mongo.db.anime.insert(anime)

                return "'{0}' has been added".format(anime['title'])
            except Exception as e:
                return str(e)
        else:
            return "All the required fields have not been completed"


    def delete(self, slug):
            # DELETE /anime/<name> - Deletes a specific anime
            query = {'slug': slug}

            try:
                anime = mongo.db.anime.find_one(query)

                full_image_path = os.path.join(app.config['UPLOAD_PATH'], anime['picture'])
                thumb_image_path = os.path.join(app.config['UPLOAD_PATH'], anime['thumb'])

                os.remove(full_image_path)
                os.remove(thumb_image_path)

                mongo.db.anime.remove(query)

                return anime['title'] + " has been deleted"
            except Exception as e:
                return str(e)


    def put(self, slug):
            # PUT /anime/<name> - Updates a specific anime

            pass


mod = Blueprint('api', __name__, url_prefix='/api')
anime_view = AnimeAPI.as_view('anime_api')
mod.add_url_rule('/anime/', defaults={'slug': None}, view_func=anime_view, methods=['GET'])
mod.add_url_rule('/anime/', view_func=anime_view, methods=['POST'])
mod.add_url_rule('/anime/<slug>', view_func=anime_view, methods=['GET', 'PUT', 'DELETE'])
