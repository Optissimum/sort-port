from app import app, database
import bleach
from models import User, Item
from contextlib import contextmanager
from oauth2client import client


@contextmanager
def database_session():
    """Provide a clean way to access our database so it won't fail."""
    session = database.session()
    try:
        yield session
        session.commit()
        session.flush()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def itemList(category=''):
    with database_session() as session:
        '''Returns a list of dictionaries with id, name, user, and category
         of each item, sorted by category unless the category is defined, then
         return id, name, user sorted by name.'''
        list = []
        for item in session.query(Item).\
                filter(Item.category_name == category).order_by(Item.name).all():
            list.append({
                        'name': item.name,
                        'user': item.user_email,
                        'category': item.category,
                        })
        return list


def itemInfo(name, category):
    with database_session() as session:
        query = Item.query.order_by(Item.name).\
            filter(Item.name == name, Item.category_name == category).first()
        item = {
            'id': query.id,
            'name': query.name,
            'category': query.category,
            'user': query.user_email,
            'description': query.description
        }
        return item


def addItem(name, userEmail, category, description):
    '''Takes strings for ease of use'''
    with database_session() as session:
        name = bleach.clean(name).lower()
        userEmail = bleach.clean(userEmail).lower()
        category = bleach.clean(category).lower()
        description = bleach.clean(description).lower()

        try:
            itemInfo(name, category)
            return Exception
        except:
            item = Item(name=name,
                        user_email=userEmail,
                        category=category,
                        description=description)
            session.add(item)
            return True


def editItem(ogName, ogCategory, name, userEmail, category, description):
    with database_session() as session:
        name = bleach.clean(name).lower()
        userEmail = bleach.clean(userEmail).lower()
        category = bleach.clean(category).lower()
        description = bleach.clean(description).lower()

        item = Item.query.filter(
            name == ogName, category == ogCategory).first()
        item.name = name
        item.userEmail = userEmail
        item.category = category
        item.description = description


def removeItem(id, userEmail):
    with database_session() as session:
        item = Item.query.filter_by(id=id).first()
        if userEmail == item.user_email:
            session.delete(item)

def userList():
    with database_session() as session:
        session.query(User).all()


def itemsByUser(user_id):
    with database_session() as session:
        return session.query(Item, User).\
            order_by(Item.name).filter(Item.user == user_id).all()


def userOfItem(item_id):
    with database_session() as session:
        return session.query(Item, User).\
            order_by(Item.name).filter(Item.id == item_id).all()


def categoryList():
    with database_session() as session:
        query = session.query(Item).group_by(Item.category_name).all()
        return [item.category for item in query]


def userList():
    with database_session() as session:
        query = session.query(User).all()
        return [(user.email, user.name) for user in query]
