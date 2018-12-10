from flask_restplus import Api

from .things import api as things
from .events import api as events
from .assets import api as assets

api = Api(
    title='Smart API',
    version='1.0',
    prefix='/api/v1',
    description='Restfull API used to query things, ecexute events and manageing assets'
)

api.add_namespace(things)
api.add_namespace(events)
api.add_namespace(assets)