from flask_restplus import Namespace, Resource, fields
from flask import request
import requests

api = Namespace('things', description='things related operations')

thing_data = api.model('data', {
            "name": fields.String,
            "valueType": fields.String, 
            "valueUnit": fields.String,
            "value":fields.String
        }
    )

thing_event_parameter = api.model("parameters", {
                    "name": fields.String,
                    "type": fields.String
                })

thing_event = api.model("events", {
            "name": fields.String,
            'parameters': fields.List(fields.Nested(thing_event_parameter))
        }
    )

thing = api.model('thing', {
    "thingId" : fields.String(required=True, description='The thing identifier'),
    "description": fields.String(required=True, description='The thing description'),
    "created": fields.String,
    "updated": fields.String,
    "data": fields.List(fields.Nested(thing_data)),
    "events": fields.List(fields.Nested(thing_event))
})

thing_list = api.model('List of things', {
    'things': fields.List(fields.Nested(thing))
})

DATA = {
    "name": "temp",
    "valueType": "double",
    "valueUnit": "celsius",
    "value": "38"
}

THING = {
    "thingId" : "38d61641-1475-452f-8ccd-a74ed59f31ca",
    "description": "Fridge in the kitchen",
    "created": "2018-04-23T18:25:43.511Z",
    "updated": "2018-04-27T18:25:43.511Z",

    "data": [
        {
            "name": "temp",
            "valueType": "double", 
            "valueUnit": "celsius",
        },
        {
            "name": "light",
            "valueType": "boolean", 
        },
        {
            "name": "running",
            "valueType": "boolean", 
        }
    ],

    "events": [
        {
            "name": "running",
            "parameters": [
                {
                    "name": "value",
                    "type": "boolean"
                }
            ]
        }
    ]
}



@api.route('/')
@api.response(404, 'Category not found.')
class Thinglist(Resource):

    @api.marshal_with(thing_list)
    def get(self):
        """
        Returns a category with a list of posts.
        """
        return THING
    

@api.route('/<id>')
@api.response(404, 'thing not found.')
class ThingItem(Resource):

    @api.marshal_with(thing)
    def get(self, id):
        """
        Returns a category with a list of posts.
        """
        return THING


@api.route('/<id>/<name>')
@api.response(404, 'thing not found.')
class ThingItemValue(Resource):

    @api.marshal_with(thing_data)
    def get(self, id, name):
        """
        Returns a category with a list of posts.
        """
        return DATA


""" 
@api.route('/')
class ThingList(Resource):
    @api.doc('list_devices')
    @api.marshal_with(thing_list)
    def get(self):
        return True
     
"""
""" 
@api.route('/<id>')
@api.param('id', 'The thing identifier')
@api.response(404, 'Mapped Device not found')
class Thing(Resource):
    @api.doc('get_thing')
    @api.marshal_with(thing)
    def get(self, id):
        '''Fetch a thing given its identifier'''
        get_thing(id)


def get_thing(id):
    pass
    '''
    for thing in DOGS:
        if dog['id'] == id:
            return dog
    '''

 """