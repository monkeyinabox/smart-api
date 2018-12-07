"""The mongo database module provides all functions to work with `pymongo <https://api.mongodb.com/>`_.
The public interface to the functionality is given by the interface module.

.. moduleauthor:: Mobile App Team

References
----------------
- decorators: https://www.python.org/dev/peps/pep-0318/
- wrapper: https://docs.python.org/3.6/library/functools.html
- mongodb: https://api.mongodb.com/python/current/
"""

from functools import wraps
from pymongo import MongoClient
from pymongo.collection import ObjectId
from db.errors import DatabaseNoConnection
from db.interface import Database, USER, TOKEN 


class MongoDb(Database):
    """The MongoDb provides the ability to store and load data in a dictionary format.

    .. seealso:: Module: :py:class:`api.repository`
    """

    def __init__(self, config):
        """Initializes the MongoDB. Adds the required collections and validators

        :param config: Configuration
        :type config: DbConfig
        
        .. seealso:: Database configuration: :py:class:`db.config.DbConfig`
        """

        self.client = MongoClient(config.HOST, config.PORT, connect=False)
        self.database = self.client[config.DATABASE]
        #self.client.drop_database(config.DATABASE)

        # inspiration by: https://jira.mongodb.org/browse/PYTHON-1064
        db_collections = self.database.collection_names()
        for key, value in COLLECTIONS.items():
            if key not in db_collections:
                self.database.create_collection(key) # creating a new collection if not exists
            self.database.command(value)             # adding a validator schema

    def validate_connection(f):
        """This decorator function checks the connection state of the database.
        
        :param f: wrapped function
        :type f: func
        :returns: Returns the the wrapped function
        :raises DatabaseNoConnection: Exception if the database client is not connected
        """
        @wraps(f)
        def func(self, *args, **kwargs):
            state = self.database.command({"connectionStatus": 1})
            if state["ok"] != 1:
                raise DatabaseNoConnection("Database is not running")
            return f(self, *args, **kwargs)
        return func

    @validate_connection
    def load(self, entity, key, value):
        """This function loads dict formatted data out of the database and replaces the database internal id *_id* with *id*.
        
        .. note:: If *key* is None all entries of the collection are returned.

        :param entity: Collection name
        :type entity: str
        :param key: Key for which the value is needed
        :type key: str
        :param value: value of the key
        :type value: object
        :returns: Returns a list of dicts
        """
        # if the key is None, all collection values are loaded
        if key is not None:
            if key == "id":
                key = "_id"
                value = ObjectId(value)
            result = self.database[entity].find({key: value})
            l = list()
            if result is not None:
                for value in result:
                    value["id"] = str(value.pop("_id"))
                    l.append(value)
            return l
        else:
            result = self.database[entity].find()
            l = list()
            if result is not None:
                for value in result:
                    value["id"] = str(value.pop("_id"))
                    l.append(value)
            return l

    @validate_connection
    def save(self, entity, key, model):
        """This function saves dict formatted data into the database. 
        
        .. note::
                  
            - If the model does not contain the *key* a new entry is inserted.
            
            - If the model contains the *key* and its value is not None then an existing entry is updated. When no entry is found a new entry is inserted.
            
            - If the model contains the *id key* and its value is not None then an existing entry is updated. When no entry is found None will be returned.
    
        :param entity: Collection name
        :type entity: str
        :param key: Identifier to check if exists
        :type key: str
        :param model: Object to be saved
        :type model: Object
        :return: ObjectId
        """
        result = None
        mdict = dict(model)
        if key in mdict and not (key == "id" and mdict[key] is None):
            arg = mdict[key]
            if key == "id" and arg is not None:
                db_result = self.database[entity].find_one_and_update({"_id": ObjectId(arg)}, {'$set': mdict}, upsert= False)
            else:
                db_result = self.database[entity].find_one_and_update({key: arg}, {'$set': mdict}, upsert=True, return_document=True)
            if db_result is not None:
                result = db_result["_id"]
        else:
            db_result = self.database[entity].insert(mdict)
            result = db_result
        return result

    @validate_connection
    def delete(self, entity, key, value):
        """This function deletes a single document depended on the *key value* pair.
        
        :param entity: Collection name
        :type entity: str
        :param key: Identifier to check if exists
        :type key: str
        :param value: value of the key
        :type value: object
        :return: ObjectId
        """
        if key == "id":
            db_result = self.database[entity].delete_one({"_id": ObjectId(value)})
        else:
            db_result = self.database[entity].delete_one({key: value})
        result = db_result.deleted_count > 0
        return result


__USER_SCHEMA = {
    "collMod": USER,
    "validator": {
        "fname": {"$type":"string",},
        "pname": {"$type": "string"},
        "age": {"$type": "int"},
        "username": {"$type": "string"},
        "password": {"$type": "string"},
        "role_group": {"$type": "string"}
    }
}

__TOKEN_SCHEMA = {
    "collMod": TOKEN,
    "validator": {
        "token": {"$type": "string"},
        "username": {"$type": "string"}
    }
}



COLLECTIONS = {USER: __USER_SCHEMA, TOKEN: __TOKEN_SCHEMA}