import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_path = os.environ.get('DATABASE_URL')
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
    Migrate(app,db)
    db.create_all()


'''
Actor
Have name, age, and gender created for actor in database
'''


class Actor(db.Model):
  __tablename__ = 'actor'

  id = Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  age = db.Column(db.String)
  gender = db.Column(db.String)

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
      self.session.delete(self)
      self.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }

  def __repr__(self):
      return f"<Actor {self.id} name: {self.name}>"


'''
Movie
Have title, and release date created for movie in database
'''


class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String)
    releasedate = db.Column(db.String)

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
        de.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'releasedate': self.releasedate
        }
    def  __repr__(self):
        return f"<Movie {self.id} title: {self.title}>"
