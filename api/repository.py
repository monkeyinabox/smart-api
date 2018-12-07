"""This module provides all the repository classes.
The access from each repository to the database is provided by an interface which is built of meta decorators. These meta
decorators define static arguments like the entity and the column of a database table. The database call itself
is done by an wrapped function which calls after successful completion the actual function in the repository.

.. note::
    Due the fact the database result is always a list of dictionaries (json) and the data only needs to be transferred
    to a requesting client, it is better to feed the api with the row dictionary (see the functions get_by...dict).
    If data is use by other reasons it is preferred to parse the data to a model (see the functions get_by...)

.. seealso:: Database interface :py:mod:`db.interface`

.. moduleauthor: Mobile App Team
"""
from api.models import User, Token
import db
import logging

logger = logging.getLogger(__name__)


class UserRepository(object):
    ENTITY = db.interface.USER

    @db.interface.load(ENTITY, "username")
    def get_by_username(self, userid, dbresult=None) -> User:
        user = User()
        if len(dbresult) > 0:
            user.adopt_dict(dbresult[0])
            return user
        return None

    @db.interface.load(ENTITY, "username")
    def get_by_username_dict(self, userid, dbresult=None) -> {}:
        if len(dbresult) > 0:
            return dbresult[0]
        return None

    @db.interface.load(ENTITY)
    def get_all(self, dbresult=None) -> ():
        users = []
        for value in dbresult:
            user = User()
            user.adopt_dict(value)
            users.append(user)
        return users

    @User.validate
    @db.save(ENTITY, "username")
    def add(self, user, object_id=None):
        return object_id

    @db.delete(ENTITY, "id")
    def delete(self, id, result=None):
        return result


class TokenRepository(object):
    ENTITY = db.interface.TOKEN

    @db.interface.load(ENTITY, "username")
    def get_by_username(self, username, dbresult=None) -> Token:
        token = Token()
        if len(dbresult) > 0:
            token.adopt_dict(dbresult[0])
            return token
        return None

    @db.interface.load(ENTITY, "token")
    def get_username_by_token(self, token, dbresult=None) -> Token:
        if len(dbresult) > 0:
            return dbresult[0]["username"]
        return None

    @db.interface.load(ENTITY)
    def get_all(self, dbresult=None) -> ():
        tokens = []
        for value in dbresult:
            token = Token()
            token.adopt_dict(value)
            tokens.append(token)
        return tokens

    @Token.validate
    @db.interface.save(ENTITY, "id")
    def add(self, token, object_id=None):
        return object_id


repositories = {}
repositories["user"] = UserRepository()
repositories["token"] = TokenRepository()
