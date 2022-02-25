import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from auth import bearer_tokens

from flaskr import create_app
from models import setup_db, Question, Category


assistant_auth = {
    'Authorization': bearer_tokens['casting_assistant']
}

director_auth = {
    'Authorization': bearer_tokens['casting_director']
}

producer_auth = {
    'Authorization': bearer_tokens['executive_producer']
}

class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency"
        self.database_path = "postgresql://{}/{}".format('localhost:5432',
                                                         self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):

        actor = {
            'name': 'Denzel Washington',
            'age': '67',
            'gender': 'Male'
        }

        actor.insert()

        res = self.client().get('/actor')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actor = Actor.query.all()
        self.assertEqual(len(data['actor']), len(actor))


    def test_get_movies(self):

        movie = {
            'title': 'Babylon'
            'releasedate': 'Decemeber 25, 2022'
        }

        movie.insert()

        res = self.client().get('/movie')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        movie = Movie.query.all()
        self.assertEqual(len(data['movie']), len(movie))


    def test_add_actor(self):

        actor_details = {
            'name': 'Input name successfully'
            'age': 'Input age successfully'
            'gender': 'Input gender successfully'
        }

        res = self.client().post('/add_actor', data=json.dumps(add_actor), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor_details['name'])
        self.assertEqual(data['actor']['age'], actor_details['age'])
        self.assertEqual(data['actor']['gender'], actor_details['gender'])

        add_actor = Actor.query.get(data['actor']['id'])
        self.assertTrue(add_actor)


    def test_add_movie(self):

        movie_details = {
             'title': 'Input title successfully'
             'releasedate': 'Input release date successfully'
        }

        res = self.client().post('/add_movie', data=json.dumps(add_movie), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], movie_details['title'])
        self.assertEqual(data['movie']['releasedate'], movie_details['releasedate'])

        add_movie = Movie.query.get(data['movie']['id'])
        self.assertTrue(add_movie)


    def test_update_actor(self):

        update_actor = {
            'age': 45
        }

        res = self.client().patch('/actor/1', data=json.dumps(update_actor), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        self.assertEqual(data['updated'], 1)


    def test_update_movie(self):

        update_movie = {
            'releasedate':
        }

        res = self.client().patch('/movie/1', data=json.dumps(update_movie), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)
        self.assertEqual(data['updated'], 1)


    def test_delete_actor(self):

        res = self.client().delete('/actor/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'], 3)


    def test_delete_movie(self):

        res = self.client().delete('/movie/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'], 3)


    def test_get_actors_auth_failure(self):
        res = self.client().get('/actor?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization is needed')

    def test_get_actors_page_failure(self):

        res = self.client().get('/actor?page=1490394839')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'not found')


    def test_get_movies_page_failure(self):

        res = self.client().get('/movie?page=895859393')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'not found')


    def test_add_actor_auth_failure(self):

        actor_details = {
            'name': 'Mario Lopez',
            'age': 36,
            'gender': 'male'
        }

        res = self.client().post('/actor', json=actor_details, headers=director_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization is needed.')


    def test_add_movie_auth_failure(self):

        movie_details = {
            'title': 'The new movie',
            'releasedate': 'September 3, 2022'
        }

        res = self.client().post('/movie', json=movie_details, headers=producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')
