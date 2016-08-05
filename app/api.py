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
    try:
        return Item.query.filter_by(name=item.name,
                                    category_name=item.category_name).count()
    except:
        return False


def addItem(item):
    with database_session() as session:
        if Item.query.filter_by(id=getItemId(item)).count():
            return False
        else:
            session.add(item)
            return True
#
#
# def addCategory(name):
#     with database_session() as session:
#         if Category.query.filter_by(name=name).count():
#             return False
#         else:
#             session.add(Category(name))
#             return True
