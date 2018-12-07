"""The interface module provides the access to the database functions. The interface works as follows:
Each interface function consists of a meta decorator and two nested functions. The meta decorator defines static 
attributes like entity or table column. The first nested function is called decorator and points to the caller function
(e.g a function in the repository). The second nested function is called wrapper, it wraps the caller function and 
does the database calls. After a successful database request the wrapper invokes the actual caller.

.. warning:: **The arguments of caller and wrapper must be the same.**

.. moduleauthor:: Mobile App Team

References
----------
- decorators: https://www.python.org/dev/peps/pep-0318/
- wrapper: https://docs.python.org/3.6/library/functools.html
"""

from abc import ABC, abstractmethod
from functools import wraps
from db.errors import DbInterfaceError
import db

# Global database variable. Only one instance in the module can exists.
database = None
USER = "user"
TOKEN = "token"


def run_database(config):
    """Instantiated a database class with a certain configuration.
    This function has to be called before the first access to the database.

        :param config: Configuration.
        :type config: DbConfig.

    .. seealso:: db.config.DbConfig
    """

    global database
    if config.MEMORYDB:
        database = db.MemoryDb(config)
    elif config.MONGODB:
        database = db.MongoDb(config)


def load(entity, key=None):
    """This decorator function provides the load interface to the database. 
    It contains a decorator and a wrapper function. If a function is called which uses this decorator, 
    the wrapped function (func) is called first and passes the database result back to the caller.
    
    :param entity: Database entity.
    :type entity: str.
    :param key: Key after which data is searched.
    :type key: object.
    :return: decorator function.
    """

    def decorator(f):
        @wraps(f)
        def func(caller=None, value=None, dbresult=None, *args, **kwargs):
            """Wrapped caller function.
            
            :param caller: Caller of the wrapped function.
            :type caller: Object.
            :param value: Value of the key for which data is searched.
            :type value: Object.
            :param dbresult: The database result is passed by this parameter.
            :type dbresult: List of dictionaries.
            :param args: 
            :return: Returns the result of the wrapped function.
            :raises DbInterfaceError: An exception is raised if the key and value constellation do not match.
            """

            if (key is None and value is not None) or (key is not None and value is None):
                raise DbInterfaceError("Invalid argument constellation: key and value")
            dbresult = db.interface.database.load(entity, key, value)
            if key is None:
                return f(caller, dbresult, *args, **kwargs)
            else:
                return f(caller, value, dbresult, *args, **kwargs)

        return func

    return decorator


def save(entity, key):
    """This decorator function provides the save interface to the database. 
    It contains a decorator and a wrapper function. If a function is called which uses this decorator, 
    the wrapped function (func) is called first.

    :param entity: Database entity.
    :type entity: str.
    :param key: Key to search an existing document.
    :type key: str.
    :return: Decorator function.
    """

    def decorator(f):
        @wraps(f)
        def func(caller, model, *args, **kwargs):
            """Wrapped caller function.
            
            :param caller: Caller of the wrapped function.
            :type caller: Object.
            :param model: The model which has to be saved.
            :type model: Object.
            :return: Returns the result of the wrapped function.
            """
            object_id = db.interface.database.save(entity, key, model)
            return f(caller, model, object_id, *args, **kwargs)
        return func
    return decorator


def delete(entity, key):
    """This decorator function provides the interface to the delete function of the database. 
    It contains a decorator and a wrapper function. If a function is called which uses this decorator, 
    the wrapped function (func) is called first.
    
    :param entity: Database entity.
    :type entity: str.
    :param key: Key to search an existing document.
    :type key: str.
    :return: Decorator function.
    """

    def decorator(f):
        @wraps(f)
        def func(caller, value, *args, **kwargs):
            """Wrapped caller function.
            
            :param caller: Caller of the wrapped function.
            :type caller: Object.
            :param value: Value of the key for which data is searched.
            :type value: Object.
            :return: Returns the result of the wrapped function.
            """
            result = db.interface.database.delete(entity, key, value)
            return f(caller, value, result, *args, **kwargs)
        return func
    return decorator


class Database(ABC):
    """ This class is used by all database classes and provides the public methods.

    """

    @abstractmethod
    def load(self, entity, key, value):
        pass

    @abstractmethod
    def save(self, entity, key, model):
        pass

    @abstractmethod
    def delete(self, entity, key, value):
        pass
