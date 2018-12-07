from flask_restplus import Namespace, Resource, fields

api = Namespace('event', description='event related operations')

event_parameter = api.model("parameters", {
                    "name": fields.String,
                    "type": fields.String
                })


event = api.model('event', {
            "cid": fields.String,
            "tid": fields.String, 
            "name": fields.String,
            "parameters": fields.List(fields.Nested(event_parameter))
        }
    )


from cloudant.client import CouchDB
from flask import request
import requests

@api.route('/')
@api.response(404, 'Category not found.')
class Event(Resource):

    @api.marshal_with(event)
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