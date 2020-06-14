import os
from secure import CONNECT_STRING, APP_DEBUG
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = APP_DEBUG

# Connect to the database
SQLALCHEMY_DATABASE_URI = CONNECT_STRING
SQLALCHEMY_TRACK_MODIFICATIONS=False
