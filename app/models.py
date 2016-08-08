from app import app, database, blueprint, cache
from flask_dance.consumer.backend.sqla import (OAuthConsumerMixin,
                                               SQLAlchemyBackend)
from flask_login import LoginManager, UserMixin, current_user
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class User(database.Model, UserMixin):
    __tablename__ = 'user'

    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(256), unique=True)
    name = database.Column(database.String(256))

    def __init__(self, name, email):
        self.name = name
        self.email = email

class OAuth(database.Model, OAuthConsumerMixin):
    __tablename__ = 'oauth'

    user_id = database.Column(database.Integer, database.ForeignKey(User.id))
    user = database.relationship(User)


class Item(database.Model):
    __tablename__ = 'item'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256))
    description = database.Column(database.String(256))
    category_name = database.Column(database.String(256),
                                    database.ForeignKey('category.name'))
    category = database.relationship('Category', backref='category')

    user_email = database.Column(database.String(256),
                                 database.ForeignKey('user.email'))
    user = database.relationship("User", uselist=False, backref="user")

    def __init__(self, name, category, description, user):
        self.name = name
        self.category_name = category
        self.description = description
        self.user = user

class Category(database.Model):
    __tablename__ = 'category'

    name = database.Column(database.String(256), primary_key=True)

    def __init__(self, name):
        self.name = name


class ItemForm(Form):
    name = TextField(
        'Item', validators=[DataRequired()]
    )
    category = TextField(
        'Category', validators=[DataRequired()]
    )
    user = SelectField(
        'Owner', validators=[DataRequired()]
    )
    description = TextAreaField(
        'Description', validators=[DataRequired()]
    )
    submit = SubmitField()
    delete = SubmitField()


class UserForm(Form):
    name = TextField(
        'Name', validators=[DataRequired()]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

blueprint.backend = SQLAlchemyBackend(OAuth, database.session,
                                      cache=cache, user=current_user)

database.create_all()
