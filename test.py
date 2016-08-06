from app.api import *
import random
import string
from app.models import Item, Category, User

# ITEM TESTS

# for _ in xrange(10):
#     cat = Category("".join([random.choice(string.letters) for i in xrange(5)]))
#
#     user = User("".join([random.choice(string.letters) for i in xrange(7)]),
#                 "@".join([random.choice(string.letters) for i in xrange(15)]))
#
#     name = "".join([random.choice(string.letters) for i in xrange(6)])
#     desu = "".join([random.choice(string.letters) for i in xrange(6)])
#
#     it = Item(name,
#               cat,
#               desu,
#               user)
#
#     addItem(it)

name = "".join([random.choice(string.letters) for i in xrange(7)])
email = "".join([random.choice(string.letters) for i in xrange(3)]) + "".join([random.choice(string.letters) for i in xrange(6)])

user = User(name,email)

print addUser(user)

user = User(name,email)

print addUser(user)
