from flask import Flask
from flask_dance.contrib.google import make_google_blueprint, google
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Flask-Dance data
app.secret_key = "qwertyuiop"
blueprint = make_google_blueprint(
    client_id="my-key-here",
    client_secret="my-secret-here",
    scope=["profile", "email"]
)

# SQLAlchemy Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
engine = create_engine("postgresql+psycopg2://user:password@/dbname")
db = SQLAlchemy(app)

from app import views
