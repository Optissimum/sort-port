from app import app, blueprint, db
from flask import render_template, redirect, url_for, flash
from flask_dance.contrib.google import google
from flask_dance.consumer import oauth_authorized, oauth_error
from sqlalchemy.orm.exc import NoResultFound
from flask_login import (
    LoginManager, current_user,
    login_required, login_user, logout_user
)
import models

# Flask Login and Dance setup and views
app.register_blueprint(blueprint, url_prefix="/login")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'google.login'

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

# Created views
@app.route('/',
           methods=['GET', 'POST'])
@app.route('/catalog/',
           methods=['GET', 'POST'])
@app.route('/index/',
           methods=['GET', 'POST'])
def catalog():
    return render_template('index.html')

@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with {name}".format(name=blueprint.name))
        return
    # figure out who the user is
    resp = google.get("/plus/v1/people/me")
    if resp.ok:
        email = resp.json()["emails"][0]["value"]
        query = models.User.query.filter_by(email=email)
        try:
            user = query.one()
        except NoResultFound:
            # create a user
            user = models.User(email=email)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash("Successfully signed in with Google")
    else:
        msg = "Failed to fetch user info from {name}".format(name=blueprint.name)
        flash(msg, category="error")

@app.route('/logout/')
@login_required
def logout():
    resp = google.get("/plus/v1/people/me")
    msg = "{name} logged out".format(name=resp.json()["emails"][0]["value"])
    logout_user()
    flash(msg)
    return redirect(url_for('catalog'))
