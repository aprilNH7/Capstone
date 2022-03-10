import os
import unittest
import json
from app import create_app
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from config import tokens
from models import setup_db, Actor, Movie


assistant_auth = {
    'Authorization': tokens['assistant_auth']
}

director_auth = {
    'Authorization': tokens['director_auth']
}

producer_auth = {
    'Authorization': tokens['producer_auth']
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

        res = self.client().get('/actor', headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_get_movies(self):

        res = self.client().get('/movie', headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_add_actor(self):

        actor_details = {
            'name' : 'Mary Jane',
            'age' : 86
        }

        res = self.client().post('/actor', json=actor_details, headers=director_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_add_movie(self):

        movie_details = {
             'title': 'New Movie',
             'releasedate': 'May 3, 2022'
        }

        res = self.client().post('/movie', json=movie_details, headers=producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_update_actor(self):

        update_actor = {
            'age': 45
        }

        res = self.client().patch('/actor/1', json=update_actor, headers=director_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        self.assertEqual(data['updated'], 1)


    def test_update_movie(self):

        update_movie = {
            'releasedate': 'April 12, 2022'
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
        res = self.client().get('/actor')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization is needed')

    def test_get_actors_page_failure(self):

        res = self.client().get('/actor?page=1490394839')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')


    def test_get_movies_page_failure(self):

        res = self.client().get('/movie?page=895859393')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')


    def test_add_actor_auth_failure(self):

        actor_details = {
            'name': 'Mario Lopez',
            'age': 36,
        }

        res = self.client().post('/actor', json=actor_details)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization is needed.')


    def test_add_movie_auth_failure(self):

        movie_details = {
            'title': 'The new movie',
            'releasedate': 'September 3, 2022'
        }

        res = self.client().post('/movie', json=movie_details, headers=director_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

if __name__ == "__main__":
    unittest.main()
