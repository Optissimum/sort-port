from flask import Flask
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache
from contextlib import contextmanager
from secrets import secrets

app = Flask(__name__)

# Flask-Dance data
app.secret_key = secrets['secret_key']
blueprint = make_google_blueprint(
    client_id=secrets['login_id'],
    client_secret=secrets['login_secret'],
    scope=["profile", "email"],
    reprompt_consent=True
)

# SQLAlchemy Setup
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///sebastian"
database = SQLAlchemy(app)

# Flask Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

from app import views, models, api
