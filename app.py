import os
from flask import Flask, request, jsonify, abort
from auth import AuthError, requires_auth
from models import setup_db, Actor, Movie
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from config import tokens


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {'origins': '*'}})


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/actor', methods=['GET'])
    def recieve_actors():
        actor = Actor.query.all()

        if not actor:
            abort(404)

        return jsonify({
            'success': True,
            'actor': [actors.format() for actors in actor]
        }), 200


    @app.route('/movie', methods=['GET'])
    def recieve_movies():
        movie = Movie.query.all()

        if not movie:
            abort(404)

        return jsonify({
            'success': True,
            'movie': [movies.format() for movies in movie]
        }), 200

    @app.route('/actor', methods=['POST'])
    @requires_auth('post:actor')
    def add_actor(payload):
        body = request.get_json()

        if not body:
            abort(400)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', 'Other')

        if not name or not age:
             abort(422)

        new_actor = (Actor(name = name, age = age, gender = gender))
        new_actor.insert()

        return jsonify({
            'success': True,
            'created': new_actor.id
        })


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
    def update_actor(payload):
        details = request.get_json()

        if not id:
            abort(404)

        try:
            actor = Actors.query.filter(Actors.id==id).one_or_none()
            actor_formatted = actor.format()

            if not actor:
                abort(404)

            name = details.get('name', actor.name)
            age = details.get('age', actor.age)
            gender = details.get('gender', actor.gender)

            actor.name = name
            actor.age = age
            actor.gender = gender

            actor.update()

        except Exception:
            abort(422)


        return jsonify({
            'success': True,
            'updated': actor
        }), 200


    @app.route('/movie/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(payload):

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
    def remove_actor(payload):

        if not id:
            abort(400)

        remove_actor = Actor.query.filter(Actor.id == id).one_or_none()

        if not remove_actor:
            abort(400)

        remove_actor.delete()

        return jsonify({
            'success': True,
            'deleted': id
        }), 200

    @app.route('/movie/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def remove_movie(payload):

        if not id:
            abort(400)

        remove_movie = Movie.query.filter(Movie.id == id).one_or_none()

        if not remove_movie:
            abort(400)

        remove_movie.delete()

        return jsonify({
            'success': True,
            'deleted': id
        }), 200


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


    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
