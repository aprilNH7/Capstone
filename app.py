import os
from flask import Flask
from auth import AuthError, requires_auth
from models import setup_db
from flask_cors import CORS
from flask import jsonify

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
            'actor': [actor.format() for actors in actor]
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

    @app.route('/add-actor', methods=['POST'])
    @requires_auth('post:actor')
    def add_actor():
        details = request.get_json()

        actor = Actor(
            name=details['name'],
            age=details['age'],
            gender=details['gender']
        )

        if 'name' not in details:
            abort(422)

        if 'age' not in details:
            abort(422)

        if 'gender' not in details:
            abort(422)

        actor.insert()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    @app.route('/add-movie', methods=['POST'])
    @requires_auth('post:movie')
    def add_movie():
        details = request.get_json()

        movie = Movie(
            title=details['title'],
            releasedate=details['releasedate']
        )
        if 'title' not in details:
            abort(422)

        if 'releasedate' not in details:
            abort(422)

        movie.insert()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    @app.route('/actor/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(actor_id):
        details = request.get_json()

        if not actor_id:
            abort(404)
        try:
            actor = Actor.query.get(actor_id)

        except Exception:
            abort(422)

        if not actor:
            abort(404)

        if 'name' in details and details['name']:
            actor.name = details['name']

        if 'age' in details and details['age']:
            actor.age = details['age']

        if 'gender' in details and details['gender']:
            actor.gender = details['gender']

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200


    @app.route('/movie/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(movie_id):

        details = request.get_json()

        if not movie_id:
            abort(404)

        try:
            movie = Movie.query.get(movie_id)

        except Exception:
            abort(422)

        if not movie:
            abort(404)

        if 'title' in details and details['title']:
            movie.title = details['title']

        if 'releasedate' in details and details['releasedate']:
            movie.releasedate = details['releasedate']

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200


    @app.route('/actor/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def remove_actor(actor_id):

        if not actor_id:
            abort(400)

        remove_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not remove_actor:
            abort(400)

        remove_actor.delete()

        return jsonify({
            'success': True,
            'deleted': actor_id
        }), 200

    @app.route('/movie/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def remove_movie(movie_id):

        if not movie_id:
            abort(400)

        remove_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not remove_movie:
            abort(400)

        remove_movie.delete()

        return jsonify({
            'success': True,
            'deleted': movie_id
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
