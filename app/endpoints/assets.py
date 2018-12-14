from flask_restplus import Namespace, Resource, fields
from cloudant.client import CouchDB
from flask import request

api = Namespace('Assets', description='asset managmenet operations')

assets_location = api.model('location', {
            "value": fields.String
})

assets = api.model('assets', {
            "_id": fields.String(required=True),
            "tid": fields.String, 
            "location": fields.List(fields.Nested(assets_location))
        }
    )

"""
CouchDB Connecntion initializeiton
"""
client = CouchDB('admin', 'admin', url='http://10.0.0.12:5984', connect=True)
session = client.session()
mydb = client['assets']


@api.route('/')
@api.response(404, 'Asset not found.')
class MapList(Resource):

    @api.marshal_with(assets)
    def get(self):
        """
        Returns a list of all assets.
        """
        data = []
        for document in mydb:
            data.append(document)
            print(document)
        return data
    
    @api.expect(assets)
    @api.response(204, 'New asset created sucessfully')
    @api.response(302, 'Asset id already exists')
    def post(self):
        """
        Create new asset mapping
        """
        data = request.json
        
        tmp_doc = data['_id'] in mydb
        if tmp_doc:
            return 302
        
        mydb.create_document(data)
        return None, 204


@api.route('/<id>')
@api.response(404, 'Asset not found.')
class MapItem(Resource):
    
    @api.response(200, 'Asset found')
    @api.marshal_with(assets)
    def get(self, id):
        """
        Returns a spesific assed by id
        """
        try:
            if mydb[id]:
                return mydb[id], 200
        except KeyError:
            return None, 404
        
    @api.expect(assets)
    @api.response(204, 'Asset successfully updated.')
    def put(self, id):
        """
        Update an existing asset
        """
        data = request.json
        my_document = mydb[id]
        my_document = data
        my_document.save()
        return None, 204

    @api.response(204, 'Asset successfully deleted.')
    def delete(self, id):
        """
        Deletes an asset.
        """
        try:
            if mydb[id]:
                my_document = mydb[id]
                my_document.delete()
                return None, 204
        except KeyError:
            return None, 404
        