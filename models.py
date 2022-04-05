import os
from sqlalchemy import Column, String, Integer, create_engine, Float
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
import json
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS


database_path = os.getenv('DATABASE_URL')


if database_path and database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)


if not database_path:
    database_name = "agency"
    database_path = "postgresql://{}/{}".format('localhost:5432', database_name)


db = SQLAlchemy()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    Migrate(app, db)
    db.create_all()


'''
Actor
Have name, age, and gender created for actor in database
'''


def test_details():
    actor1 = Actors(name='Timmy', age=20, gender='Male')
    actor1.insert()


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    def __repr__(self):
        return f'<Actor id: {self.id}, name: {self.name}, age: {self.age}, gender: {self.gender}>'

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
         'id': self.id,
         'name': self.name,
         'age': self.age,
         'gender': self.gender
        }


'''
Movie
Have title, and release date created for movie in database
'''


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    releasedate = db.Column(db.String)

    def __repr__(self):
        return f'<Movie id: {self.id}, title: {self.title}, releaseDate: {self.releaseDate}>'

    def __init__(self, title, releasedate):
        self.title = title
        self.releasedate = releasedate

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'releasedate': self.releasedate
        }
