from app import app, blueprint, database
from app.dbapi import *
import app.dbapi as dbapi
from flask import render_template, redirect, url_for, flash, request
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
    return render_template('categorylist.html',
                           categoryList=categoryList())


@app.route('/add/', methods=['GET', 'POST'])
@app.route('/catalog/add/', methods=['GET', 'POST'])
@login_required
def addItem():
    form = models.ItemForm(request.form)
    form.user.choices = userList()
    if request.method == 'POST':
        try:
            form.validate_on_submit()
            dbapi.addItem(
                form.name.data,
                form.user.data,
                form.category.data,
                form.description.data)
            return redirect(url_for('viewItem',
                                    category=form.category.data,
                                    itemName=form.name.data))
        except:
            flash('The item {0} already exists within the {1}'
                  ' category'.format(str(form.name.data).title(),
                                     str(form.category.data).title()))
    return render_template("add.html", form=form)


@app.route('/catalog/<string:category>/<string:itemName>/edit', methods=['GET', 'POST'])
@login_required
def editItem(category, itemName):
    form = models.ItemForm(request.form)
    form.user.choices = userList()
    item = itemInfo(itemName, category)
    if request.method == 'POST':
        try:
            form.validate_on_submit()
            dbapi.editItem(
                itemName,
                category,
                form.name.data,
                form.user.data,
                form.category.data,
                form.description.data)
            return redirect(url_for('viewItem',
                                    itemName=form.name.data,
                                    category=form.category.data))
        except:
            flash('The item {0} already exists within the {1}'
                  ' category'.format(str(form.name.data).title(),
                                     str(form.category.data).title()))
    return render_template('edit.html',
                           form=form,
                           item=item)


@app.route('/catalog/<string:category>/<string:itemName>/')
def viewItem(category, itemName):
    user = ''
    try:
        user = google.get("/plus/v1/people/me").json()["emails"][0]["value"]
    except:
        flash('To edit this item, please log in')

    return render_template('view.html',
                           item=itemInfo(name=itemName, category=category),
                           user=user)


@app.route('/catalog/<string:category>/')
def viewCategory(category):
    # TODO create category list
    return render_template('itemlist.html',
                           category=categoryList(),
                           items=itemList(category),
                           currentCategory=category.title())


# Login views
@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with {name}".format(name=blueprint.name))
        return
    # figure out who the user is
    resp = google.get("/plus/v1/people/me")
    if resp.ok:
        email = resp.json()["emails"][0]["value"]
        name = resp.json()["name"]["givenName"]
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
    return render_template('login.html')
