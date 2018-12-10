from flask_restplus import Api

from .thing import api as things
from .event import api as events
from .mapping import api as mapping

api = Api(
    title='Smart API',
    version='1.0',
    description='A simple demo API',
)

api.add_namespace(things)
api.add_namespace(events)
api.add_namespace(mapping)