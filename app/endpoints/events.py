from flask_restplus import Namespace, Resource, fields
from flask import request
import requests

from app import config

api = Namespace('Events', description='executing events on controller')


event_parameter = api.model("parameters", {
                    "value": fields.String,
                })

event = api.model('event', {
            "cid": fields.String,
            "tid": fields.String, 
            "name": fields.String,
            "parameters": fields.List(fields.Nested(event_parameter))
        }
    )

CONTROLLER_URL = config.CONTROLLER_URL

@api.route('/')
@api.response(400, 'Event execution failed')
class Event(Resource):
    @api.expect(event)
    def put(self):
        """
        Executes an event on controller and return data if avaiable.
        """
        data = request.json
        response = requests.put(CONTROLLER_URL, params=data)
        if not response.ok:
            return None, 400
        else:
            return response.json(), 200
