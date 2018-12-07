from flask_restplus import Api

from .thing import api as things


api = Api(
    title='Smart API',
    version='1.0',
    description='A simple demo API',
)

api.add_namespace(things)
