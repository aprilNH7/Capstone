import os
from flask import Flask, request, jsonify, abort
from auth import AuthError, requires_auth
from models import *
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import tokens


def paginate_actor(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ACTOR_PER_PAGE
    end = start + ACTOR_PER_PAGE

    actor = [actor.format() for actor in selection]
    current_actor = actor[start:end]

    return current_actor

ACTOR_PER_PAGE = 10

def paginate_movie(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * MOVIE_PER_PAGE
    end = start + MOVIE_PER_PAGE

    movie = [movie.format() for movie in selection]
    current_movie = movie[start:end]

    return current_movie


MOVIE_PER_PAGE = 10


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {'origins': '*'}})


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/actor', methods=['GET'])
    def recieve_actors():
        selection = Actor.query.all()
        actor = paginate_actor(request, selection)

        if len(actor) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'actor': actor
        }), 200


    @app.route('/movie', methods=['GET'])
    def recieve_movies():
        selection = Movie.query.all()
        movie = paginate_movie(request, selection)

        if len(movie) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'movie': movie
        }), 200

    @app.route('/actor', methods=['POST'])
    @requires_auth('post:actor')
    def add_actor(payload):
        details = request.get_json()

        name = details.get('name', None)
        age = details.get('age', None)
        gender = details.get('gender', None)

        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            selection = Actor.query.all()
            current_actor = paginate_actor(request, selection)

            return jsonify({
              'success': True,
              'created': actor.id,
              'actor': current_actor,
              'total_actors': len(Actor.query.all())
            }), 200

        except:
            abort(400)


    @app.route('/movie', methods=['POST'])
    @requires_auth('post:movie')
    def add_movie(payload):
        details = request.get_json()

        if not id:
            abort(400)

        movie = Movie(
            title=details['title'],
            releasedate=details['releasedate']
        )

        movie.insert()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200


    @app.route('/actor/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(payload, id):
        details = request.get_json()

        if not id:
            abort(404)

        try:
            actor = Actor.query.get(id)

            if not actor:
                abort(404)

            name = details.get('name', actor.name)
            age = details.get('age', actor.age)
            gender = details.get('gender', actor.gender)

            actor.name = name
            actor.age = age
            actor.gender = gender

            actor.update()

            return jsonify({
                'success': True,
                'updated': actor.format()
            }), 200

        except Exception:
            abort(422)


    @app.route('/movie/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(payload, id):

        details = request.get_json()

        if not id:
            abort(404)

        try:
            movie = Movie.query.get(id)

            if not movie:
                abort(404)

            title = details.get('title', movie.releasedate)
            releasedate = details.get('releasedate', movie.releasedate)

            movie.title = title
            movie.releasedate = releasedate

            movie.update()

        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200


    @app.route('/actor/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def remove_actor(payload, id):

        if not id:
            abort(400)

        actor_delete = Actor.query.filter(Actor.id == id).one_or_none()

        actor_delete.delete()

        if not actor_delete:
            abort(404)


        return jsonify({
          'success': True,
          'deleted': id
        })



    @app.route('/movie/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def remove_movie(payload, id):

        if not id:
            abort(400)

        movie_delete = Movie.query.filter(Movie.id == id).one_or_none()

        movie_delete.delete()

        if not movie_delete:
            abort(404)

        return jsonify({
          'success': True,
          'deleted': id
        })


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code


    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
