from flask_restplus import Namespace, Resource, fields
from cloudant.client import CouchDB
from flask import request

api = Namespace('mapping', description='things related operations')

mapping_location = api.model('location', {
            "value": fields.String
})

mapping = api.model('mapping', {
            "cid": fields.String,
            "tid": fields.String, 
            "location": fields.List(fields.Nested(mapping_location))
        }
    )

client = CouchDB('admin', 'admin', url='http://127.0.0.1:5984', connect=True)
session = client.session()
mydb = client['devices']

@api.route('/')
@api.response(404, 'Category not found.')
class MapList(Resource):

    @api.marshal_with(mapping)
    def get(self):
        """
        Returns a category with a list of posts.
        """
        data = []
        for document in mydb:
            data.append(document)
            print(document)
        return data
    
    @api.expect(mapping)
    @api.response(204, 'Category successfully updated.')
    def post(self):
        data = request.json
        mydb.create_document(data)
        return None, 204



@api.route('/<id>')
@api.response(404, 'Category not found.')
class MapItem(Resource):

    @api.marshal_with(mapping)
    def get(self, id):
        """
        Returns a category with a list of posts.
        """
        return mydb[id]

    @api.expect(mapping)
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