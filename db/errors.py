"""The module errors defines the database Exeptions. 

.. moduleauthor:: Mobile App Team
"""

class DbInterfaceError(Exception):
    """Is raised if an key value constellation is detected.
    
    """
    def __init__(self, message):
        super(DbInterfaceError, self).__init__(message)

class DatabaseNoConnection(Exception):
    """Is raised if a database interface function is executed and no connection to the database exists.

    """
    def __init__(self, message):
        super(DatabaseNoConnection, self).__init__(message)


