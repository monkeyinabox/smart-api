"""This module provides the flask web functionality and the flask-restful api functionality along with some basic functions.
For the basic route functions, three decorators are used. The ordering of the decorators has to be as printed below
otherwise the functionality of the route is not ensured.

- Defines the REST resource:            @flask_app.route
- Validates the token Authorization:    @flask_auth.login_required
- Validates user role:                  @requires_role
- Check for valid json content          @validate_json

.. moduleauthor: Mobile App Team
"""
import requests

from functools import wraps

from flask import Flask, make_response, jsonify, request, g
from flask_httpauth import HTTPTokenAuth
from flask_restful import Api
from flask_cors import CORS

from logging import *
from jsonschema.exceptions import ValidationError
from api.authentication import check_user_and_password
from api.repository import repositories
from api.errors import AuthenticationException
from util.errors import ParsingException

flask_app = Flask(__name__, instance_relative_config=True)
cors = CORS(flask_app, resources={r"/*": {"origins": "*"}})

flask_api = Api(flask_app)
flask_auth = HTTPTokenAuth("Bearer")

logger = getLogger(__name__)

tokens_str = []

user_group_roles = {
    "administrator": [
        "load",
        "save",
        "delete"
    ],
    "readonly": [
        "load"
    ]
}

def validate_json(f):
    """ This decorator validates the header content of a post whether the format is JSON
    
    :param f: Wrapped post function
    :return: function
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            logger.log(INFO, "Wrong content-type, needs to be 'application/json'")
            return response_error("Wrong content type sent, needs to be application/json")
        try:
            logger.log(INFO, "Getting JSON data from request")
            data = request.json
        except Exception as e:
            logger.exception(e)
            return response_error("Please send valid JSON data with POST request")
        return f(*args, **kwargs)

    return decorated


def requires_role(role=None, group=None):
    """This decorator validates whether the current user is allowed to perform the request.
    Before executing this function, the login_required function has to be executed to ensure the current user.
    
    It can be chosen between a special role oder a whole user group to manage the access. If the group is not None, it
    has priority.
    
    .. note::
        taken by "http://flask.pocoo.org/snippets/98/" and modified
    
    :param role: User role
    :type role: str
    :param group: User group 
    :type group: str
    :return: 
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            message = jsonify({"status": "error", "message": "Unauthorized user level"})
            user = repositories["user"].get_by_username(g.user)
            if group is not None:
                if group != user.role_group:
                    return make_response(message, 401)
            elif user.role_group not in user_group_roles or role not in user_group_roles[user.role_group]:
                return make_response(message, 401)

            return f(*args, **kwargs)
        return wrapped
    return wrapper


def response_error(message: str, data=None):
    """Creates an error message as response and logs the message.
    """
    logger.log(ERROR, message)
    if data is None:
        return jsonify({"status": "error", "message": message})
    else:
        return jsonify({"status": "error", "message": message, "data": data})


def response_notice(message: str, data=None):
    """Creates an notice message as response and logs the message.
    """
    logger.log(INFO, message)
    return jsonify({"status": "notice", "message": message, "data": data})


def response_success(message: str, data=None):
    """Creates a success message as response.
    """
    if data is None:
        return jsonify({"status": "success", "message": message})
    else:
        return jsonify({"status": "success", "message": message, "data": data})


def get_tokens_as_str_arr():
    """Queries the database for all tokens and returns their token parameter as an array of strings. This string is
    stored as a global variable (array) for faster future use.

    :returns: Returns the result of the query or false if the query could not complete
    """
    logger.log(INFO, "Getting all tokens and storing them in global variable")
    global tokens_str
    tokens_str = []
    tokens_str.clear()

    try:
        logger.log(INFO, "Querying database for tokens")
        tokens = repositories["token"].get_all()
    except Exception as e:
        logger.exception(e)
        return False

    if type(tokens) is bool and tokens is False:
        logger.log(INFO, "Query for tokens returned false")
        return False
    else:
        tokens_str.clear()
        for tmp_token in tokens:
            tokens_str.append(tmp_token.token)
        return tokens_str


@flask_auth.verify_token
def verify_token(token):
    """Checks if the token which was sent in the request is valid. It first checks the local token string array for
    matching files for speed reason (no database access needed, all in memory). If no token is found the database is
    queried in the function :method::^get_tokens_as_str_arr^ and the token is checked again.

    :param:	token – token from request header as str
    :returns: true if valid token, else false
    """
    logger.log(INFO, "Verifying token: " + token)
    # current user taken by -> https://flask-httpauth.readthedocs.io/en/latest/
    g.user = repositories["token"].get_username_by_token(token)
    global tokens_str
    if token in tokens_str:
        logger.log(INFO, "Found valid token")
        return True
    else:
        tokens_str = get_tokens_as_str_arr()

    if token in tokens_str:
        logger.log(INFO, "Found valid token")
        return True
    else:
        return False


@flask_app.errorhandler(404)
def not_found(error):
    """Returns the client an http error code 404 and a JSON data answer if a non-existing view is requested

    :returns: JSON data and http code 404 (not found)
    """
    return make_response(jsonify({"status": "error", "message": "Not found"}), 404)


@flask_auth.error_handler
def unauthorized():
    """Returns the client an http error code 401 and a json data answer if the user has no rights to access the
    requested content

    :returns: JSON data and http code 401 (forbidden)
    """
    return make_response(jsonify({"status": "error", "message": "Unauthorized access"}), 401)


@flask_app.route('/')
@flask_auth.login_required
def index():
    """The / (root) route. To access this the user needs to authenticate via valid bearer token in the header of the
    request. This route is mostly used to check if the API responds to requests and to check the validity of the token.

    Check out the `API Reference`_ for further information on how to work with the API

    .. _`API Reference`: api_reference.html

    :returns: JSON data and http code 202
    """
    return make_response(jsonify({"status": "success", "message": "Validation accepted"}), 202)


@flask_app.route('/user/auth/')
def user_auth():
    """The /auth/ (authentication) route. This route accepts basic authentication, checks user / password with the
    database and returns a token. It also returns appropriate responses if the request missed or contained wrong
    authentication info. Uses helper function :meth:`api.authentication.check_user_and_password()` See the respective
    documentation for more information.

    Check out the `API Reference`_ for further information on how to work with the API

    .. _`API Reference`: api_reference.html

    :returns: JSON data
    :raises: AuthenticationException
    """
    try:
        logger.log(INFO, "Getting authorization info from request")
        auth_data = request.authorization
    except AuthenticationException as e:
        logger.exception(e)
        return response_error("Error on getting authorization info from request")

    if auth_data is not None:
        logger.log(INFO, "Received authentication info, checking for user: " + auth_data.username)
        message = check_user_and_password(auth_data)
        return message
    else:
        logger.log(INFO, "No basic authentication received with request")
        return response_notice("No basic authentication received with request")



@flask_app.route('/user/save/', methods=["POST"])
@flask_auth.login_required
@requires_role(group="administrator")
@validate_json
def user_save():
    """The /user/save/ route saves a new situation or updates an existing situation.
    If an id is sent in the post request and the id is found in the database, the situation will be updated.
    Otherwise if the id is invalid and not existing in the database, None is returned.
    If the id key is missing in the content a new graph database entry will be created.
    
    Check out the `API Reference`_ for further information on how to work with the API

    .. _`API Reference`: api_reference.html

    :return: success response with graph id
    :raises: ValidationError
    """
    logger.log(INFO, "Saving a user")
    try:
        data_as_dict = dict(request.json)

        # user validating and saving
        object_id = repositories["user"].add(data_as_dict)

        # check for successful saving
        if "id" in data_as_dict and object_id is None:
            return response_notice("User id not found", data_as_dict["id"])
        elif object_id is None:
            return response_error("User not saved")

    except ValidationError as e:
        logger.exception(e.message)
        return response_error("Not valid keys in dict, check API reference", e.message)
    except Exception as e:
        logger.exception(e)
        return response_error(str(e))
    return response_success("user saved", str(object_id))

@flask_app.route('/user/load/<string:username>/', methods=["GET"])
@flask_auth.login_required
@requires_role(group="administrator")
def user_load(username):
    """The /user/load/ route loads a user by username.

    Check out the `API Reference`_ for further information on how to work with the API

    .. _`API Reference`: api_reference.html

    :param username: username
    :type username: str
    :return: Returns the found user object as dict
    """

    try:
        logger.log(INFO, "Querying database for user with username " + username)
        user = repositories["user"].get_by_username_dict(username)
    except Exception as e:
        logger.exception(e)
        return response_error(str(e))

    if user is None:
        return response_notice("User not found", username)

    user.pop('password')
    return response_success("User found, returning object", user)

@flask_app.route('/user/list/', methods=["GET"])
@flask_auth.login_required
@requires_role(group="administrator")
def user_list():
    """The /user/list/ route returns a list of all users on the server.

    Check out the `API Reference`_ for further information on how to work with the API

    .. _`API Reference`: api_reference.html

    :returns: JSON data
    :raises: QueryException
    """
    # Getting list of situations
    try:
        logger.log(INFO, "Querying database for users")
        users = repositories["user"].get_all()
    except Exception as e:
        logger.exception(e)
        return response_error(str(e))

    users_list = []
    for user in users:
        username = user.username
        users_list.append(username)
    return response_success("Users found, returning list of users", users_list)


@flask_app.route('/user/delete/<string:userid>/', methods=["DELETE"])
@flask_auth.login_required
@requires_role(group="administrator")
def user_delete(userid):
    """The /user/delete/ route deletes a graph by id.

    Check out the `API Reference`_ for further information on how to work with the API

    .. _`API Reference`: api_reference.html

    :return: success response with graph id
    """
    logger.log(INFO, "Delete user with id " + userid)
    try:
        # graph validating and saving
        result = repositories["user"].delete(userid)

        if not result:
            return response_notice("User id not found", userid)

    except Exception as e:
        logger.exception(e)
        return response_error(str(e))

    return response_success("User found and deleted", result)


@flask_app.route('/fan/status/<string:status>/', methods=["PUT"])
@flask_auth.login_required
@requires_role(group="administrator")
def set_fan_status(status):
    """The /user/delete/ route deletes a graph by id.

    Check out the `API Reference`_ for further information on how to work with the API

    .. _`API Reference`: api_reference.html

    :return: success response with graph id
    """
    logger.log(INFO, "Delete user with id " + status)
    try:
    
        #result = repositories["user"].delete(userid)
        parameters =  { 
            "event": 
            {
                "cid":  "xyz",
                "tid":  123,
                "name": "activate",
                "parameter": True 
            }
        }

        response = requests.put("http://isorp.ch:1880/event/", params=parameters)

        #if not result:
        #    return response_notice("User id not found", userid)

    except Exception as e:
        logger.exception(e)
        return response_error(str(e))

    return response_success("status changed", response.ok)