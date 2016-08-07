from app import database
import api
import models
from utils import *
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
from sqlalchemy.orm.exc import NoResultFound


# Flask Login and Dance setup and views
app.register_blueprint(blueprint, url_prefix="/login")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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
    return render_template('catalog.html',
                           categories=api.viewCategories())


@app.route('/add',
           methods=['GET', 'POST'])
def add():
    form = models.ItemForm(request.form)
    form.user.choices = api.userList()
    if request.method == 'POST':
        form.validate_on_submit()
        item = models.Item(
            form.name.data,
            form.user.data,
            form.category.data,
            form.description.data
        )
        if api.addItem(item):
            flash('Success!')
            # TODO: Create viewItem.html and link appropriately
            # redirect(url_for('viewItem',
            #                         category=form.category.data,
            #                         itemName=form.name.data))
        else:
            flash('Error adding {0}. Maybe it already exists within {1}?'.format(
                str(form.name.data).title(), str(form.category.data).title()))
    return render_template("add.html", form=form)


@app.route('/catalog/<string:category>/<string:name>/',
           methods=['GET'])
@templated()
def viewItem(category, name):

    return api.getItem(name=name, category=category)


@app.route('/catalog/<string:category>/',
           methods=['GET', 'POST'])
def viewCategory(category):
    return render_template('viewCategory.html',
                           items=api.viewCategory(category),
                           categories=api.viewCategories())


# Login views, partially pulled from flask-dance quick-start example
@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with {name}".format(name=blueprint.name))
        return
    resp = google.get("/plus/v1/people/me")
    if resp.ok:
        name = resp.json()["name"]["givenName"]
        email = resp.json()["emails"][0]["value"]
        user = models.User(name, email)
        print user
        # api.addUser(user)
        query = models.User.query.filter_by(email=email)
        try:
            user = query.one()
        except NoResultFound:
            # create a user
            user = models.User(email=email, name=name)
            database.session.add(user)
            database.session.commit()
        login_user(user)
        flash("Successfully signed in with Google")
    else:
        msg = "Failed to fetch user info from {name}".format(
            name=blueprint.name)
        flash(msg, category="error")


@app.route('/logout/')
@login_required
def logout():
    try:
        resp = google.get("/plus/v1/people/me")
        msg = "{name} logged out".format(
            name=resp.json()["emails"][0]["value"])
    except:
        msg = 'Logged out'
    logout_user()
    flash(msg)
    return redirect(url_for('catalog'))


@app.route('/login/')
def login():
    return redirect(url_for('google.login'))
