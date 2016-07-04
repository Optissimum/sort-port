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
        '''Returns a dictionary of id, name, owner, and category
         sorted by category unless the category is defined, then
         return id, name, owner sorted by name.'''
        return session.query(Item).\
            filter(Item.category == category).order_by(Item.name).all()

def itemInfo(name, category):
    with database_session() as session:
        return session.query(Item).order_by(Item.name).\
            filter(Item.name == name, Item.category == category).first()

def addItem(name, ownerEmail, category, description):
    '''Takes strings for ease of use'''
    with database_session() as session:
        if itemInfo(name, category) is not None:
            return Exception
        else:
            name = bleach.clean(name).lower()
            ownerEmail = bleach.clean(ownerEmail).lower()
            category = bleach.clean(category).lower()
            description = bleach.clean(description).lower()
            item = Item(name=name,
                        owner_email=ownerEmail,
                        category=category,
                        description=description)
            session.add(item)
            return True

def editItem(id, name, ownerEmail, category):
    with database_session() as session:
        if session.query(Item).filter(Item.owner_email):
            session.update(Item).where(Item.id == id).value(
                name=name, category=category)

def removeItem(owner_id, item_id):
    with database_session() as session:
        session.delete(Item).filter(
            Item.item.id == item_id, owner_id == Item.owner)

def addOwner(name, email):
    with database_session() as session:
        bleach.clean(name, email)
        if ownerExists(email):
            owner = Owner(name=name, email=email)
            session.add(owner)
            return True
        else:
            return False

def removeOwner(owner_id):
    with database_session() as session:
        session.delete(Owner).filter(owner_id == id)

def ownerList():
    with database_session() as session:
        session.query(Owner).all()

def itemsByOwner(owner_id):
    with database_session() as session:
        return session.query(Item, Owner).\
            order_by(Item.name).filter(Item.owner == owner_id).all()

def ownerOfItem(item_id):
    with database_session() as session:
        return session.query(Item, Owner).\
            order_by(Item.name).filter(Item.id == item_id).all()

def ownerExists(email):
    with database_session() as session:
        return session.query(Owner).filter(Owner.email == email).first()

def categoryList():
    with database_session() as session:
        query = session.query(Item).group_by(Item.category).all()
        return [item.category for item in query]
