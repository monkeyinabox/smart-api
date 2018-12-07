from flask_restplus import Namespace, Resource, fields

api = Namespace('things', description='things related operations')

thing_data = api.model('data', {
            "name": fields.String,
            "valueType": fields.String, 
            "valueUnit": fields.String
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


from cloudant.client import CouchDB
from flask import request

client = CouchDB('admin', 'admin', url='http://localhost:5984', connect=True)
session = client.session()
mydb = client['devices']

@api.route('/')
@api.response(404, 'Category not found.')
class Thinglist(Resource):

    @api.marshal_with(thing)
    def get(self):
        """
        Returns a category with a list of posts.
        """
        data = []
        for document in mydb:
            data.append(document)
            print(document)
        return data
    
    @api.expect(thing)
    @api.response(204, 'Category successfully updated.')
    def post(self):
        data = request.json
        mydb.create_document(data)
        return None, 204



@api.route('/<id>')
@api.response(404, 'Category not found.')
class ThingItem(Resource):

    @api.marshal_with(thing)
    def get(self, id):
        """
        Returns a category with a list of posts.
        """
        return mydb[id]

    @api.expect(thing)
    @api.response(204, 'Category successfully updated.')
    def put(self, id):
        data = request.json
        my_document = mydb[id]
        my_document = data
        my_document.save()
        return None, 204

    @api.response(204, 'Category successfully deleted.')
    def delete(self, id):
        """
        Deletes blog category.
        """
        my_document = mydb[id]
        my_document.delete()
        return None, 204


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