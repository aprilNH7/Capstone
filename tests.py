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

        details = {
            'name': 'Alicia Keys',
            'age': 35,
            'gender': 'Female'
        }
        res = self.client().post('/actor', json=details, headers=director_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_add_movie(self):
        details = {
             'title': 'March Madness',
             'releasedate': 'September 12, 2022'
        }

        res = self.client().post('/movie', json=details, headers=producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_actor(self):
        patch_actor = {
            'name': 'Jenny Karry',
            'age': 18
        }

        res = self.client().patch('/actor/11', json=patch_actor,
                                  headers=director_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_movie(self):
        patch_movie = {
            'releasedate': 'July 29, 2022'
        }

        res = self.client().patch('/movie/15', json=patch_movie,
                                  headers=producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_actor(self):
        res = self.client().delete('/actor/60', headers=director_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 60)

    def test_delete_movie(self):
        res = self.client().delete('/movie/60', headers=producer_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 60)

    def test_add_actor_auth_failure(self):

        details = {
            'name': 'Taylor Mason',
            'age': 74,
            'gender': 'Female'
        }

        res = self.client().post('/actor', json=details,
                                 headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_add_movie_auth_failure(self):
        details = {
            'title': 'Dad',
            'releasedate': 'July 26, 2022'
        }

        res = self.client().post('/movie', json=details, headers=director_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_404_get_actor_beyond_valid_page(self):
        res = self.client().get('/actor?page=100000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_404_get_movie_beyond_valid_page(self):
        res = self.client().get('/movie?page=28475973', headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_actor_auth_failure(self):
        patch_actor = {
            'name': 'Jenny Karry',
            'age': 18
        }

        res = self.client().patch('/actor/11', json=patch_actor,
                                  headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_movie_auth_failure(self):
        patch_movie = {
            'releasedate': 'July 29, 2022'
        }

        res = self.client().patch('/movie/15', json=patch_movie,
                                  headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actor_auth_failure(self):
        res = self.client().delete('/actor/11', headers=assistant_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_movie_auth_failure(self):
        res = self.client().delete('/movie/9', headers=director_auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()

