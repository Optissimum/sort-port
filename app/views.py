from app import app, blueprint, database
from flask import (
    render_template, redirect,
    url_for, flash, request,
    jsonify, abort)
from flask_dance.contrib.google import google
from flask_dance.consumer import oauth_authorized, oauth_error
from sqlalchemy.orm.exc import NoResultFound
from flask_login import (
    LoginManager, current_user,
    login_required, login_user, logout_user
)
import models
import api
from sqlalchemy.orm import exc
from werkzeug.exceptions import abort

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
                           categoryList=dbapi.categoryList())


@app.route('/add/', methods=['GET', 'POST'])
@app.route('/catalog/add/', methods=['GET', 'POST'])
@login_required
def addItem():
    form = models.ItemForm(request.form)
    form.user.choices = dbapi.userList()
    if request.method == 'POST':
        print form.name.data
        print form.user.data
        print form.category.data
        print form.description.data
        form.validate_on_submit()
        if dbapi.addItem(
                form.name.data,
                form.user.data,
                form.category.data,
                form.description.data):
            return redirect(url_for('viewItem',
                                    category=form.category.data,
                                    itemName=form.name.data))
        else:
            flash('Error adding {0}. Maybe it already exists within {1}?'.format(
                str(form.name.data).title(), str(form.category.data).title()))
    return render_template("add.html", form=form)


@app.route('/catalog/<string:category>/<string:itemName>/edit', methods=['GET', 'POST'])
@login_required
def editItem(category, itemName):
    form = models.ItemForm(request.form)
    form.user.choices = dbapi.userList()
    try:
        item = dbapi.itemInfo(itemName, category)
    except AttributeError:
        abort(404)
    if request.method == 'POST':
        form.validate_on_submit()
        if form.delete.data:
            dbapi.removeItem(id=item['id'], userEmail=item['user'])
            redirect(url_for('catalog', ))
        elif form.submit.data:
            try:
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
        item = dbapi.itemInfo(name=itemName, category=category)
    except AttributeError:
        abort(404)
    try:
        user = google.get("/plus/v1/people/me").json()["emails"][0]["value"]
    except:
        flash('To edit this item, please log in')

    return render_template('view.html',
                           item=item,
                           user=user)


@app.route('/catalog/<string:category>/')
def viewCategory(category):
    # TODO create category list
    try:
        return render_template('itemlist.html',
                               category=dbapi.categoryList(),
                               items=dbapi.itemList(category),
                               currentCategory=category.title())
    except AttributeError:
        abort()


# Login views, partially pulled from flask-dance quick-start example
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


# JSON views
@app.route('/catalog/<string:category>/<string:itemName>/json')
def getItem(name, category):
    item = dbapi.itemInfo(name, category)
    return jsonify(name=item['name'],
                   category=item['category'],
                   owner=item['user'],
                   description=item['description'])


@app.route('/catalog/<string:category>/json')
def getCategory(category):
    category = dbapi.itemList(category)
    return jsonify(name=item['name'],
                   category=item['category'],
                   owner=item['user'])
