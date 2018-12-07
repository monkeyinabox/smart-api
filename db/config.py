"""Database configuration. 

.. moduleauthor:: Mobile App Team
"""

class DbConfig:
    MEMORYDB = False
    MONGODB = False
    DATABASE = ""
    HOST = ""
    PORT = ""

class MemoryDbConfigLocal(DbConfig):
    MEMORYDB = True
    DATABASE = "wimo"

class MongoDbConfigLocal(DbConfig):
    MONGODB = True
    DATABASE = "wimo"
    HOST = "localhost"
    PORT = 27017


class DevelopmentConfig(DbConfig):
    MONGODB = True
    DATABASE = "wimo"
    HOST = "metasaurus.ch"
    PORT = 27017


class DevelopmentConfigUnittests(DbConfig):
    MONGODB = True
    DATABASE = "wimo-unittests"
    HOST = "localhost"
    PORT = 27017


dbConfigType = {
    "memory": MemoryDbConfigLocal,
    "local": MongoDbConfigLocal,
    "unittests": DevelopmentConfigUnittests,
    "development": DevelopmentConfig,
}