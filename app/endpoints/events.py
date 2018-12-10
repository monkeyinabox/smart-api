from flask_restplus import Namespace, Resource, fields
from flask import request
import requests

api = Namespace('events', description='executing events on controller')


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

CONTROLLER_URL = "http://isorp.ch:1880/events/"

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
            print(response.content)
            return response.content, 200
