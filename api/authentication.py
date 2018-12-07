import traceback

from flask import jsonify

from api.models import Token, User
from api.repository import repositories
import logging

from api.errors import DatabaseStoreException

logger = logging.getLogger(__name__)


def check_user_and_password(auth_data):
    """Queries the users from the database and checks if the sent authentication data is valid. If it is, the function
    returns the response which is sent to the client. Uses helper function :meth:`api.authentication.query_for_token()`

    A more detailed explanation: If the authentication data is not empty the database is queried for a user. As key to
    query for the user the username from the request is used. If the result from this query is a user object the method
    checks if the sent password from the authentication is valid. If username and password are valid, the method gets a
    token via helper function :meth:`api.authentication.query_for_token()` (see its documentation for the how to). In
    the end a message is returned to the route method containing the token if the authentication data is valid. If not,
    a message with relevant information what went wrong is returned.

    :param: auth_data: Authentication data from the request header (basic auth)
    :returns: Returns a message to return to the client from the route (JSON)
    """
    error_message = jsonify({"status": "error", "message": "This should not have happened, check the logs"})
    if auth_data.username != "" and auth_data.password != "":
        try:
            logger.log(20, "Querying database for user " + auth_data.username)
            user = repositories["user"].get_by_username(auth_data.username)
        except Exception as e:
            logger.exception(e)
            return error_message

        if user is None:
            logger.log(20, "User " + auth_data.username + " not found in database")
            message = jsonify({"status": "notice", "message": "User not found"})
            return message

        if type(user) is User:
            logger.log(20, "User " + auth_data.username + " found in database")
            if user.validate_password(auth_data.password):
                username = user.username
                logger.log(20, "Valid password, checking for token")
                token = query_for_token(username)

                if type(token) is Token:
                    message = jsonify({"status": "success", "message": "User authenticated, returning token", "token": token.token})
                    logger.log(20, "Returning token")
                    return message
                else:
                    logger.log(40, "Did not receive token with type str from method 'query_for_token'")
                    return error_message
            elif not user.validate_password(auth_data.password):
                logger.log(20, "Password validation returned 'False'")
                message = jsonify({"status": "notice", "message": "Wrong password"})
                return message
        else:
            logger.log(40, "Queried object is not boolean nor User object")
            return error_message
    else:
        logger.log(20, "Basic authentication empty password, username or both")
        message = jsonify({"status": "notice", "message": "Please send basic authentication"})
        return message


def query_for_token(username):
    """Queries the tokens for a token where the attribute “user_id” matches the parameter. If no such token is found one
    is created and stored in the database in the helper function :meth:`api.authentication.create_token()`

    :param:	username: ID of the user to query for in the token collection
    :returns: Returns a token string matching the user
    """
    try:
        logger.log(20, "Querying database for token with username " + str(username))
        username = str(username)

        token = repositories["token"].get_by_username(username)  # returns either the searched object or false
    except Exception as e:
        logger.exception(e)

    if token is None:
        logger.log(20, "No token found, creating a token object")
        token = create_token(username)
    if type(token) is Token:
        logger.log(20, "Token found, returning token as string")
        return token
    else:
        logger.log(40, "Found object is neither token nor bool")
        return False


def create_token(username):
    """Creates a token object and stores it in the database. This token object contains as attribute a specific user_id

    :param:	username: ID of the user for which to create a token
    :returns: token: Returns a token matching the user
    :raises: DatabaseStoreException
    """
    tmp_token = Token()
    tmp_token.username = username
    tmp_token.generate_token()
    logger.log(20, "Generated token object with username " + str(username))
    try:
        logger.log(20, "Storing token in database")
        repositories["token"].add(tmp_token)
    except DatabaseStoreException as e:
        logger.exception(e)
        return False
    logger.log(20, "Returning token object")
    return tmp_token
