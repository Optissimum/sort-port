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
        q = Item.query.get_or_404(id)
        output = {
            'id': q.id,
            'name': q.name,
            'category_name': q.category_name,
            'description': q.description,
            'user': q.user_email}
        return output


def findItem(name, category):
    with database_session() as session:
        q = Item.query.filter_by(name=item.name,
                                 category_name=item.category_name).one()
        output = {
            'id': q.id,
            'name': q.name,
            'category_name': q.category_name,
            'description': q.description,
            'user': q.user_email}
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
    '''Returns a dictionary of dicts with all the item info'''
    with database_session() as session:
        list = []
        for item in session.query(Item).\
                filter(Item.category_name == category).order_by(Item.name).all():
            list.append({
                        'name': item.name,
                        'user': item.user_email,
                        'description': item.des,
                        'category': item.category_name,
                        })
        return list


def addUser(user):
    with database_session() as session:
        if session.query(User).filter_by(email=user.email).count() is not 0:
            return False
        else:
            session.add(user)
            return True


def userList():
    with database_session() as session:
        return [(user.email, user.name) for user in session.query(User).all()]
