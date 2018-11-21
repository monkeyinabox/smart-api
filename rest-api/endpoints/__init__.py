from flask_restplus import Api

from .device import api as cat_api
from .controller import api as dog_api

api = Api(
    title='Zoo API',
    version='1.0',
    description='A simple demo API',
)

api.add_namespace(cat_api)
api.add_namespace(dog_api)
