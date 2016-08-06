from app import database
from contextlib import contextmanager
from models import Item, Category, User
from sqlalchemy.exc import IntegrityError


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
                'category_name': q.category_name,
                'description': q.description,
                'user': q.user}
            return output
        except:
            return False


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
            print addCategory(category)
            return True
        else:
            return False


def addCategory(name):
    with database_session() as session:
        if Category.query.filter_by(name=name).count():
            return False
        else:
            session.add(Category(name))
            return True
