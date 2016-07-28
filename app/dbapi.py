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
                filter(Item.category == category).order_by(Item.name).all():
            list.append({
                        'name': item.name,
                        'user': item.user_email,
                        'category': item.category,
                        })
        return list


def itemInfo(name, category):
    with database_session() as session:
        query = session.query(Item).order_by(Item.name).\
            filter(Item.name == name, Item.category == category).first()
        item = {
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
            print 'Item already exists'
            return Exception
        except:
            item = Item(name=name,
                        user_email=userEmail,
                        category=category,
                        description=description)
            session.add(item)
            print 'Item added'
            return True


def editItem(id, name, userEmail, category):
    with database_session() as session:
        if session.query(Item).filter(Item.user_email):
            session.update(Item).where(Item.id == id).value(
                name=name, category=category)


def removeItem(user_id, item_id):
    with database_session() as session:
        session.delete(Item).filter(
            Item.item.id == item_id, user_id == Item.user)


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
        query = session.query(Item).group_by(Item.category).all()
        return [item.category for item in query]


def userList():
    with database_session() as session:
        query = session.query(User).all()
        return [(user.name, user.email) for user in query]
