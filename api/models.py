"""This module contains all entities classes. 

.. moduleauthor:: Mobile App Team

References
----------------
- Decorators        : https://www.python.org/dev/peps/pep-0318/
- Abstract classes  : http://intermediatepythonista.com/metaclasses-abc-class-decorators
- Json schema       : http://json-schema.org
- Json validation   : https://github.com/Julian/jsonschema

.. note::

    To see the structure of the models check out :doc:`models`. The schemas
    in this document are the ones used for the JSON validation of documents.
    They are accurate, but not easily readable.

"""




import random
import time
import logging
import jsonschema
from abc import ABC
from functools import wraps

logger = logging.getLogger(__name__)


class BaseModel(ABC):
    """BaseModel class for all entity models. 
    Provides base functionalities such as dictionary adoption and validation
    """

    def __init__(self):
        self.id = None

    def __getitem__(self, key):
        """Returns the attributes value by key. value=self[key].
        
        :param key: 
        :return: Value of an attribute
        """
        return getattr(self, key)

    def __setitem__(self, key, value):
        """ Supports item assignment when calling self[key]=value
        The function is moreover used for dict adoption (adopt_dict).
        
        :param key: 
        :param value: 
        """
        setattr(self, key, value)

    def adopt_dict(self, data: dict):
        """Adopts values of a dict and validates the dict structure. 
        If the key value structure of the dict does not match with the model, a exception will be raised.
        
        :param data:
        :type data: dict
        :raise  AttributeError, ValidationError:
        """
        # Json-schema validation
        self._validate(data)

        # dict adoption, raises AttributeError if the attribute is not found
        for key, value in data.items():
            getattr(self, key)
            self[key] = value

    @classmethod
    def _validate(cls, data: dict):
        """Validates a dict with the current model schema.

        :param data:.
        :type data: dict.
        :raise ValidationError:
        """
        # Json-schema validation
        jsonschema.validate(data, cls.SCHEMA)

    @classmethod
    def validate(cls, f):
        """This decorator validates a dict with the associated model. If the key value structure of the dict does not 
        match with the model, a exception will be raised.
        
        :param f: Wrapped function
        :raise AttributeError, ValidationError:  
        """
        @wraps(f)
        def func(inst, data, *args, **kwargs):
            cls._validate(dict(data))
            return f(inst, data, *args, **kwargs)
        return func


class User(BaseModel):
    """The User model provides the ability to modify and change users and as well validating the secret password.

    .. seealso:: User repository: :py:class:`api.repository.UserRepository`
    """

    SCHEMA = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "additionalProperties": False,
        "type": "object",
        "required": ["fname", "pname", "age", "username", "password", "role_group"],
        "properties": {
            "id": {"type": ["string", "null"]},
            "fname": {"type": "string"},
            "pname": {"type": "string"},
            "age": {"type": "integer"},
            "username": {"type": "string"},
            "password": {"type": "string"},
            "role_group": {"type": "string"}
        }
    }

    def __init__(self):
        super().__init__()
        self.fname = ""
        self.pname = ""
        self.age = 0
        self.username = ""
        self.password = ""
        self.role_group = "readonly"

    def __iter__(self):
        """The __iter__ method is used to allow iteration over the attributes given here.
        This is used to convert __name__ objects to dict objects

        """
        yield "id", self.id
        yield "fname", self.fname
        yield "pname", self.pname
        yield "age", self.age
        yield "username", self.username
        yield "password", self.password
        yield "role_group", self.role_group

    def validate_password(self, password):
        """Validates a given password against the user object

        :param password: Password (as string) to check
        :return: returns true or false
        :rtype: bool
        """
        if self.password == password:
            return True
        return False


class Token(BaseModel):
    """The Token model describes the model used to create tokens. Tokens are used for authentication and identification
    tasks.

      .. seealso:: Token repository: :py:class:`api.repository.TokenRepository`
      """

    SCHEMA = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "additionalProperties": False,
        "type": "object",
        "required": ["token", "username"],
        "properties": {
            "id": {"type": ["string", "null"]},
            "token": {"type": "string"},
            "username": {"type": "string"}
        }
    }

    def __init__(self):
        super().__init__()
        self.token = ""
        self.username = ""

    def __iter__(self):
        """The __iter__ method is used to allow iterization over the attributes given here. 
        This is used to convert __name__ objects to dict objects

        """
        yield "id", self.id
        yield 'token', self.token
        yield 'username', self.username

    def generate_token(self):
        """This method generates a token. Tokens need to be unique. They are created as follows:

        A random string of 20 hexadecimal characters is created. Afterwards, the current unix timestamp is added to the
        string. This way uniqueness is guaranteed.

        :return: random number
        """
        length = 20
        timestamp = int(time.time())
        rand_number = "".join(random.SystemRandom().choice('1234567890abcdef') for _ in range(length))
        rand_number = rand_number + timestamp.__str__()
        self.token = rand_number
        return rand_number
