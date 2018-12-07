import unittest
from pprint import pprint

from api import config
from api import app
import db
from bson import ObjectId
from db.config import dbConfigType
from api.errors import AuthenticationException

from api.repository import repositories
from api.models import User, Token
from api.authentication import check_user_and_password, query_for_token, create_token
from flask import Request, jsonify


class AuthenticationTest(unittest.TestCase):
    def setUp(self):
        db.run_database(dbConfigType["memory"])
        app.flask_app.config.from_object(config.flask_config_type["testing"])

    def test_create_token(self):
        user_id = "id_1234"
        result = create_token(user_id)
        self.assertTrue(isinstance(result, Token))

    def test_query_for_token(self):
        user_id = "id_1234"
        create_token(user_id)

        result = query_for_token(user_id)
        self.assertTrue(isinstance(result, Token))

        """The following will create a new token and does NOT check for the validity of the user_id (or if it exists). 
        This is already done in the method "check_user_and_password" which itself calls the method "query_for_token" 
        """
        result = query_for_token("nonexistant user id")
        self.assertTrue(isinstance(result, Token))

    def test_check_user_and_password(self):
        auth_data = Request.authorization
        auth_data.username = "valid_user"
        auth_data.password = "valid_password"

        user = User()
        user.username = "valid_user"
        user.password = "valid_password"
        user.id = "id_1234"
        result = repositories["user"].add(user)
        self.assertTrue(isinstance(result, ObjectId))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
