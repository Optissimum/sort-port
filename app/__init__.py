from flask import Flask
from flask_dance.contrib.google import make_google_blueprint, google
from flask_sqlalchemy import SQLAlchemy
from secrets import *

app = Flask(__name__)

# Flask-Dance data
app.secret_key = secret_key
blueprint = make_google_blueprint(
    client_id=login_id,
    client_secret=login_secret,
    scope=["profile", "email"],
    reprompt_consent=True
)

# SQLAlchemy Setup
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
db = SQLAlchemy(app)

from app import views, models
