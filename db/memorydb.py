"""The memorydb module is only used for testing.
The public interface to the functionality is given by the interface module. It is provided by decorator functions.

.. moduleauthor:: Mobile App Team

References
----------------
- decorators: https://www.python.org/dev/peps/pep-0318/
- wrapper: https://docs.python.org/3.6/library/functools.html
- mongodb: https://api.mongodb.com/python/current/"""

from functools import wraps
from db import *
from db.errors import DatabaseNoConnection


class MemoryDb(Database):
    """The MemoryDb provides the ability to store and load as a dictionary for testing.
    The data remains only for the current session in the memory.

    .. note::
        The MemoryDB is currently not in use.
    
    .. seealso::
        Module :api:repository
    """

    def __init__(self, config=None):
        """Initializes the MemoryDb.
        
            :param config: Configuration.
            :type config: DbConfig.
            
            .. seealso:: db.config.DbConfig 
            """
        self.__db = {}

    def load(self, entity, key, value):
        """This function loads one data object out of the database.
        
        :param entity: Collection name.
        :type entity: str.
        :param key: Key for which the value is needed. 
        :type key: str.
        :param value: value of the key. 
        :type value: object.
        :returns: Returns a list of dicts.
        
        .. note::
            The search for a key happens only in the 1st depth of the dictionary e.g
            collection { key1 :  value }.
        """

        # if the key is None, all collection values are loaded
        if value is not None:
            result = self.__db[entity]
            l = list()
            for item in result.items():
                if key in item[1]:
                    l.append(item[1])
                return l
            return None
        else:
            result = self.__db[entity]
            l = list()
            if result is not None:
                for k, v in result.items():
                    l.append(v)
            return l

    def save(self, entity, key, model):
        """This function saves data into the database and replaces the "id" key with the database internal id "_id".

        :param entity: Collection name.
        :type entity: str.
        :param model: Object to be saved. 
        :type model: Object.
        :param id: Object identifier. 
        :type id: Object.
        """

        id = model.id
        mdict = dict(model)
        
        if not entity in self.__db.keys():
            self.__db[entity] = {}
        self.__db[entity][id] = mdict

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

        return None