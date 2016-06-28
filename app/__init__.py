from flask import Flask
from flask_dance.contrib.google import make_google_blueprint, google


app = Flask(__name__)
app.secret_key = "supersekrit"
blueprint = make_google_blueprint(
    client_id="my-key-here",
    client_secret="my-secret-here",
    scope=["profile", "email"]
)
from app import views
