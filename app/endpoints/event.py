from flask_restplus import Namespace, Resource, fields
from flask import request
import requests

api = Namespace('event', description='event related operations')


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



@api.route('/')
@api.response(404, 'Category not found.')
class Event(Resource):
    @api.expect(event)
    @api.marshal_with(event)
    def put(self):
        """
        Returns a category with a list of posts.
        """
        data = request.json
        response = requests.put("http://isorp.ch:1880/event/", params=data)
        return response
