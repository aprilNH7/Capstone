import os
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(_file_))

# Enables debug mode.
DEBUG = True

# Database URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/agency'
SQLALCHEMY_TRACK_MODIFICATIONS = False
