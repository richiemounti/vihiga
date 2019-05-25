import os
from flask import (
    Flask,
    current_app
)
from flask_session import Session
import nexmo
from config import DevelopmentConfig, Config, configs
from utils import env_var, extract_error

from app.extensions import (
    csrf_protect,
    login,
    bcrypt,
    db
)


'''
# Load in configuration from environment variables:
NEXMO_API_KEY = env_var('49653c8a')
NEXMO_API_SECRET = env_var('GoHP8xj08j7sfprG')
NEXMO_NUMBER = env_var()

# Create a new Nexmo Client object
client = nexmo.Client(
    api_key=NEXMO_API_KEY, api_secret=NEXMO_API_SECRET
)
'''
# Initialize flask

"""Creates the app object and attacges all neccessary urls
Keyword Arguments:
    config {str} -- [Config to use to create the app]
        (default: {'development'})
Returns:
    [object] -- [Flask instance]
"""
app = Flask(__name__)

app.secret_key = ("You really should change this")
app.config.from_object(
        
        configs['production']
    )
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:mulama@localhost:5432/vihigacdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from app import models

db.init_app(app)
bcrypt.init_app(app)
login.init_app(app)
csrf_protect.init_app(app)

from app.auth.auth import auth
from app.post.post import post
from app.admin.admin import admin

app.register_blueprint(post)
app.register_blueprint(auth)   
app.register_blueprint(admin)