from flask_restplus import Namespace, Resource, fields
from cloudant.client import CouchDB
from flask import request
from app import config

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
try:
    client = CouchDB(config.ASSETS_USER, config.ASSETS_PASSWD, url=config.ASSETS_URL, connect=True)
    session = client.session()
    mydb = client[config.ASSETS_DB]
except:
    print("No DB Connection possible")

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


@api.route('/thing/<thing_id>')
@api.response(404, 'Asset not found.')
class MapItemByThing(Resource):
    
    @api.response(200, 'Asset found')
    @api.marshal_with(assets)
    def get(self, thing_id):
        """
        Returns a spesific assed by thing_id
        """

        for document in mydb:
            if document['tid'] == thing_id:
                return document, 200

        else:
            return None, 404

        
    @api.expect(assets)
    @api.response(204, 'Asset successfully updated.')
    def put(self, thing_id):
        """
        Update an existing asset
        """
        data = request.json

        for document in mydb:
            if document['tid'] == thing_id:
                document = data
                document.save()
                return None, 204

        return None, 404

    @api.response(204, 'Asset successfully deleted.')
    def delete(self, thing_id):
        """
        Deletes an asset.
        """
        for document in mydb:
            if document['tid'] == thing_id:
                document.delete()
                document.save()
                return None, 204

        return None, 404


@api.route('/asset/<asset_id>')
@api.response(404, 'Asset not found.')
class MapItemByAsset(Resource):
    
    @api.response(200, 'Asset found')
    @api.marshal_with(assets)
    def get(self, asset_id):
        """
        Returns a spesific assed by asset_id
        """
        try:
            if mydb[asset_id]:
                return mydb[asset_id], 200
        except KeyError:
            return None, 404
        
    @api.expect(assets)
    @api.response(204, 'Asset successfully updated.')
    def put(self, thing_id):
        """
        Update an existing asset
        """
        data = request.json
        my_document = mydb[thing_id]
        my_document = data
        my_document.save()
        return None, 204

    @api.response(204, 'Asset successfully deleted.')
    def delete(self, thing_id):
        """
        Deletes an asset.
        """
        try:
            if mydb[thing_id]:
                my_document = mydb[thing_id]
                my_document.delete()
                return None, 204
        except KeyError:
            return None, 404