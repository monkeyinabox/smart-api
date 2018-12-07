"""This module contains custom exception classes for the package api. 

.. moduleauthor:: Mobile App Team

"""

class InvalidVertexException(Exception):
    """Defines an exception which is raised if an invalid vertex operation is detected.
    For example if an edge is called with invalid vertices ids.
    
    """
    def __init__(self, message):
        super(InvalidVertexException, self).__init__(message)

class DatabaseStoreException(Exception):
    def __init__(self, message):
        super(DatabaseStoreException, self).__init__(message)

class AuthenticationException(Exception):
    def __init__(self, message):
        super(AuthenticationException, self).__init__(message)
