from app import database
from contextlib import contextmanager
from models import Item, Category, User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


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


def getItemId(item):
    with database_session() as session:
        session.add(item)
        try:
            id = Item.query.filter_by(
                name=item.name, category_name=item.category_name).first().id
            session.flush()
            return id
        except:
            return False


def getItem(id):
    with database_session() as session:
        try:
            q = Item.query.get(id)
            output = {
                'id': q.id,
                'name': q.name,
                'category': q.category_name,
                'description': q.description,
                'user': q.user_email}
            return output
        except:
            return False


def viewItem(name=None, user=None, category=None, description=None):
    with database_session() as session:
        query = session.query(Item)
        if name is not None:
            query = query.filter_by(name=name)
        if user is not None:
            query = query.filter_by(user_email=user)
        if category is not None:
            query = query.filter_by(category_name=category)
        if description is not None:
            query = query.filter_by(description=description)
        query = query.first()
        output = {
            'id': query.id,
            'name': query.name,
            'category': query.category_name,
            'description': query.description,
            'user': query.user_email}
        return output


def addItem(item):
    with database_session() as session:
        if Item.query.filter_by(name=item.name,
                                category_name=item.category_name).count():
            return False
        else:
            session.add(item)
            return True


def editItem(id, name, desc, category, email):
    with database_session() as session:
        newItem = {
            'name': name,
            'category_name': category,
            'description': desc,
            'user_email': email
        }
        if session.query(Item).filter_by(id=id).update(newItem):
            addCategory(category)
            return True
        else:
            return False


def deleteItem(id):
    with database_session() as session:
        try:
            session.delete(Item.query.get(id))
            return True
        except Exception as e:
            raise
            return False


def addCategory(name):
    with database_session() as session:
        if Category.query.filter_by(name=name).one():
            return False
        else:
            session.add(Category(name))
            return True


def viewCategories():
    with database_session() as session:
        return [category.name for category in Category.query.all()]


def viewCategory(category):
    with database_session() as session:
        output = []
        for item in Item.query.filter(category==category).all():
            output.append(getItem(item.id))
        return output


def addUser(user):
    with database_session() as session:
        if session.query(User).filter_by(email=user.email).count() is not 0:
            return False
        else:
            session.add(user)
            return True


def userList():
    with database_session() as session:
        query = session.query(User).all()
        return [(user.email, user.name) for user in query]

def getUserId():
    with database_session() as session:
        return int(session.query(User).filter_by(email=user.email).one().id)
