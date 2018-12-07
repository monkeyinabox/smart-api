import logging

from api.models import User, Token
from api.repository import repositories

logger = logging.getLogger(__name__)

def populate_db():
    """The method populate_db creates some basic models and stores them in the database. It is executed when a certain
    route is opened (/populatedb/).

    """
    user1 = User()
    user1.id = "1"
    user1.fname = "admin"
    user1.pname = "backen2d"
    user1.username = "admin"
    user1.password = "1234"
    user1.age = 0
    user1.role_group = "administrator"

    user2 = User()
    user2.id = "2"
    user2.fname = "readonly"
    user2.pname = "backend"
    user2.username = "readonly"
    user2.password = "1234"
    user2.age = 0
    user2.role_group = "readonly"

    token1 = Token()
    token1.id = "3"
    token1.username = "admin"
    #token1.generate_token()
    token1.token = "873f7688bbe4086ab27a1544122563"

    token2 = Token()
    token2.id = "4"
    token2.username = "readonly"
    #token2.generate_token()
    token2.token = "4c078c9db4a85c59f1fd1544122586"

    repositories["user"].add(user1)
    repositories["user"].add(user2)

    repositories["token"].add(token1)
    repositories["token"].add(token2)

