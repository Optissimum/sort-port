from app import app, database
from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_login import LoginManager, UserMixin
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length


class User(database.Model, UserMixin):
    __tablename__ = 'user'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(256), unique=True)
    email = database.Column(database.String(256), unique=True)
    password = database.Column(database.String(256), unique=True)
    first_name = database.Column(database.String(256))
    last_name = database.Column(database.String(256))

class OAuth(database.Model, OAuthConsumerMixin):
    __tablename__ = 'oauth'
    user_id = database.Column(database.Integer, database.ForeignKey(User.id))
    user = database.relationship(User)

class Item(database.Model):
    __tablename__ = 'item'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256))
    description = database.Column(database.String(256))
    category = database.Column(database.String(256))
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    user = database.relationship("User", uselist=False, backref="user")

class ItemForm(Form):
    name = TextField(
        'Item', validators=[DataRequired()]
    )
    category = SelectField(
        'Category', validators=[]
    )
    owner = TextField(
        'Owner', validators=[DataRequired(), Length(min=6, max=40)]
    )
    description = TextAreaField(
        'Description', validators=[DataRequired()]
    )


class UserForm(Form):
    name = TextField(
        'Name', validators=[DataRequired()]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
