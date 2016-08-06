from app import database
import api, models
from app import app, blueprint, database
from flask import (
    render_template, redirect,
    url_for, flash, request,
    jsonify, abort)
from flask_dance.contrib.google import google
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import (
    LoginManager, current_user,
    login_required, login_user, logout_user
)
from werkzeug.exceptions import abort

# Flask Login and Dance setup and views
app.register_blueprint(blueprint, url_prefix="/login")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
