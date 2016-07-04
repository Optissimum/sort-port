from app import app, db
from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_login import LoginManager, UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256), unique=True)
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))

class OAuth(db.Model, OAuthConsumerMixin):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

class Item():
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.String(256))
    category = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", uselist=False, backref="user")
