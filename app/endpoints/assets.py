from flask_restplus import Namespace, Resource, fields
from cloudant.client import CouchDB
from flask import request
from app import config
api = Namespace('assets', description='asset managmenet operations')

assets_location = api.model('location', {
            "value": fields.String
})

assets = api.model('assets', {
            "_id": fields.String(required=True),
            "tid": fields.String, 
            "location": fields.List(fields.Nested(assets_location))
        }
    )

client = CouchDB(config.ASSETS_USER, config.ASSETS_PASSWD, url=config.ASSETS_URL, connect=True)
session = client.session()
mydb = client['devices']

@api.route('/')
@api.response(404, 'Category not found.')
class MapList(Resource):

    @api.marshal_with(assets)
    def get(self):
        """
        Returns a category with a list of posts.
        """
        data = []
        for document in mydb:
            data.append(document)
            print(document)
        return data
    
    @api.expect(assets)
    @api.response(204, 'Category successfully updated.')
    def post(self):
        data = request.json
        mydb.create_document(data)
        return None, 204



@api.route('/<id>')
@api.response(404, 'Category not found.')
class MapItem(Resource):

    @api.marshal_with(assets)
    def get(self, id):
        """
        Returns a category with a list of posts.
        """
        return mydb[id]

    @api.expect(assets)
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
        Deletes an asset.
        """
        my_document = mydb[id]
        my_document.delete()
        return None, 204
