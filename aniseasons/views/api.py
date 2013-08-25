from bson import json_util
from flask import Blueprint, request, Response, session
from flask.views import MethodView
from werkzeug import check_password_hash

from aniseasons import app, helpers, mongo

import os


class AnimeAPI(MethodView):

    def get(self, slug):
        if slug is None:
            # GET /anime - Gets a list of all the anime
            anime = mongo.db.anime.find().sort([['_id', -1]])
            return Response(json_util.dumps(anime), status=200, mimetype='application/json')
        else:
            # GET /anime/<name> - Gets a specific anime
            anime = mongo.db.anime.find_one_or_404({'slug': slug})
            return Response(json_util.dumps(anime), status=200, mimetype='application/json')


    def post(self):
        # POST /anime - Creates a new anime
        if session['logged_in']:
            if helpers.are_fields_valid(request):
                try:
                    anime = {}
                    for key, value in request.form.iteritems():
                        if key == "genre":
                            anime[key] = value.split(',');
                        else:
                            anime[key] = value

                    anime['slug'] = helpers.slugify(anime['title'])

                    saved_files = helpers.save_image_and_thumbnail(anime['slug'], request.files['file'], app.config['UPLOAD_PATH'])

                    anime['picture'] = saved_files[0]
                    anime['thumbnail'] = saved_files[1]

                    mongo.db.anime.insert(anime)
                    inserted_anime = mongo.db.anime.find_one_or_404({'slug': anime['slug']})
                    return Response(json_util.dumps(inserted_anime), status=200, mimetype='application/json')
                except Exception as e:
                    message = {'message': str(e)}
                    return Response(json_util.dumps(message), status=400, mimetype='application/json')
            else:
                message = {'message': 'All the required fields have not been completed'}
                return Response(json_util.dumps(message), status=400, mimetype='application/json')
        else:
            message = {'message': 'You are not authorized to add anime'}
            return Response(json_util.dumps(message), status=401, mimetype='application/json')


    def delete(self, slug):
        # DELETE /anime/<name> - Deletes a specific anime
        if session['logged_in']:
            query = {'slug': slug}

            try:
                anime = mongo.db.anime.find_one(query)

                full_image_path = os.path.join(app.config['UPLOAD_PATH'], anime['picture'])
                thumbnail_image_path = os.path.join(app.config['UPLOAD_PATH'], anime['thumbnail'])

                os.remove(full_image_path)
                os.remove(thumbnail_image_path)

                mongo.db.anime.remove(query)

                message = {'message': anime['title'] + ' has been deleted'}
                return Response(json_util.dumps(message), status=200, mimetype='application/json')
            except Exception as e:
                message = {'message': str(e)}
                return Response(json_util.dumps(message), status=400, mimetype='application/json')
        else:
            message = {'message': 'You are not authorized to add anime'}
            return Response(json_util.dumps(message), status=401, mimetype='application/json')


    def put(self, slug):
        # PUT /anime/<name> - Updates a specific anime
        if session['logged_in']:
            if helpers.are_fields_valid(request, True):
                try:
                    anime = {}
                    for key, value in request.form.iteritems():
                        if key == "genre":
                            anime[key] = value.split(',');
                        else:
                            anime[key] = value

                    anime['slug'] = helpers.slugify(anime['title'])

                    if request.files:
                        saved_files = helpers.save_image_and_thumbnail(anime['slug'], request.files['file'], app.config['UPLOAD_PATH'])

                        anime['picture'] = saved_files[0]
                        anime['thumbnail'] = saved_files[1]

                    mongo.db.anime.update({'slug': slug}, {'$set': anime})

                    updated_anime = mongo.db.anime.find_one_or_404({'slug': anime['slug']})
                    return Response(json_util.dumps(updated_anime), status=200, mimetype='application/json')
                except Exception as e:
                    message = {'message': str(e)}
                    return Response(json_util.dumps(message), status=400, mimetype='application/json')
            else:
                message = {'message': 'All the required fields have not been completed'}
                return Response(json_util.dumps(message), status=400, mimetype='application/json')
        else:
            message = {'message': 'You are not authorized to add anime'}
            return Response(json_util.dumps(message), status=401, mimetype='application/json')


mod = Blueprint('api', __name__, url_prefix='/api')

@mod.route('/user/login', methods=['POST'])
def login():
    message = {}
    user = mongo.db.users.find_one({'username': request.form['username']})

    if check_password_hash(user['password'], request.form['password']):
        status = 200
        session['logged_in'] = True
        message['message'] = "Login successful"
    else:
        status = 401
        message['message'] = "Login unsuccessful"

    return Response(json_util.dumps(message), status=status, mimetype='application/json')

@mod.route('/user/logout', methods=['POST'])
def logout():
    pass

anime_view = AnimeAPI.as_view('anime_api')
mod.add_url_rule('/anime/', defaults={'slug': None}, view_func=anime_view, methods=['GET'])
mod.add_url_rule('/anime/', view_func=anime_view, methods=['POST'])
mod.add_url_rule('/anime/<slug>', view_func=anime_view, methods=['GET', 'PUT', 'DELETE'])
