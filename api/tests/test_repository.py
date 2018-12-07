"""Repository test functions. 

.. moduleauthor:: Mobile App Team
"""

import copy
import unittest

import db
from api.models import Token
from api.repository import repositories
from db.config import dbConfigType
from jsonschema.exceptions import ValidationError


class TokenRepositoryTest(unittest.TestCase):
    """The TokenRepositoryTest provides the ability to check the functionality of the TokenRepository functions

    .. seealso::
        Module :api.repository
    """

    def setUp(self):
        db.run_database(dbConfigType["memory"])

    def test_functions(self):
        """Tests the functionality of all token repository functions. The MongoDb is used

        """
        # test for valid attribute
        token = Token()
        result = repositories["token"].add(token)
        self.assertIsNot(result, None)

        token_dict = {"token": "1234", "username": "testuser"}
        result = repositories["token"].add(token_dict)
        self.assertIsNot(result, None)

        token_dict_invalid_value_type = {"token": "1234", "username": 1}
        with self.assertRaises(ValidationError):
            repositories["token"].add(token_dict_invalid_value_type)

        token_dict_invalid_key = {"token": "1234", "username": "testuser", "wrong_attribute": False}
        with self.assertRaises(ValidationError):
            repositories["token"].add(token_dict_invalid_key)

        result = repositories["token"].get_all()
        self.assertTrue(isinstance(result, list))

        result = repositories["token"].get_by_username("invalid_user")
        self.assertIsNone(result)

        result = repositories["token"].get_by_username("testuser")
        self.assertTrue(isinstance(result, Token))

    def tearDown(self):
        pass
        #db.interface.database.client.drop_database(db.dbConfigType["memory"].DATABASE)


class UserRepositoryTest(unittest.TestCase):
    """The UserRepositoryTest provides the ability to check the functionality of the repository and the associated models
    
    .. seealso::
        Module :api.repository
    """

    def setUp(self):
        db.run_database(dbConfigType["memory"])

    def test_functions(self):
        """Tests the functionality of all user repository functions. The MemoryDb is used
        """

        # test for valid attribute
        user_dict = {"id":None, "fnam":"","pname":"","age":99,"username":"","password":"", "dummy":"raises exception"}
        with self.assertRaises(ValidationError):
            repositories["user"].add(user_dict)

        # test for valid type (password)
        user_dict = {"id": None, "fname":"","pname":"","age":99,"username":"","password":123}
        with self.assertRaises(ValidationError):
            repositories["user"].add(user_dict)

        # test for proper saving function
        user_dict = {"fname": "", "pname": "","age": 4, "username": "user", "password": "", "role_group": "aa"}
        result = repositories["user"].add(user_dict)
        self.assertIsNot(result, None)

        # test for proper return function
        # ..as User
        user = repositories["user"].get_by_username("user")
        self.assertEqual(user.username, "user")
        user = repositories["user"].get_all()
        self.assertIsInstance(user, list)
        self.assertEqual(user[0]["username"], "user")
        # ..as dict
        user = repositories["user"].get_by_username_dict("user")
        self.assertEqual(user["username"], "user")

        # delete
        result = repositories["user"].delete(result)
        self.assertEqual(result, True)

    def tearDown(self):
        pass
        #db.interface.database.client.drop_database(db.dbConfigType["memory"].DATABASE)


if __name__ == '__main__':
    unittest.main()