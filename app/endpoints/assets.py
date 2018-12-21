from flask_restplus import Namespace, Resource, fields
from cloudant.client import CouchDB
from flask import request
from app import config

api = Namespace('Assets', description='asset managmenet operations')

assets_location = api.model('location', {
        "value": fields.String
})

event_parameter = api.model("parameters", {
                    "value": fields.String,
                })

assets_event = api.model('event', {
            "cid": fields.String,
            "tid": fields.String, 
            "name": fields.String,
            "parameters": fields.List(fields.Nested(event_parameter))
        }
    )

assets = api.model('assets', {
        "_id": fields.String(required=True),
        "tid": fields.String, 
        "location": fields.List(fields.Nested(assets_location)),
        "event": fields.List(fields.Nested(assets_event))
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
        Update an existing asset by thing_id
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

@api.route('/<asset_id>')
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
        Update an existing asset by thing_id
        """
        data = request.json
        my_document = mydb[thing_id]
        my_document = data
        my_document.save()
        return None, 204

    @api.response(204, 'Asset successfully deleted.')
    def delete(self, thing_id):
        """
        Deletes an asset by thing_id
        """
        try:
            if mydb[thing_id]:
                my_document = mydb[thing_id]
                my_document.delete()
                return None, 204
        except KeyError:
            return None, 404


@api.route('/<asset_id>/events/')
@api.response(404, 'Asset not found.')
class MapEventByAsset(Resource):
    
    @api.response(200, 'Asset found')
    @api.marshal_with(assets_event)
    def get(self, asset_id):
        """
        Returns a spesific assed by asset_id
        """
        try:
            if mydb[asset_id]:
                return mydb[asset_id]["event"], 200
        except KeyError:
            return None, 404
        
    @api.expect(assets_event)
    @api.response(204, 'Asset successfully updated.')
    def put(self, asset_id):
        """
        Update an existing asset by asset_id
        """
        data = request.json
        asset = None
        try:
            if mydb[asset_id]:
                asset = mydb[asset_id], 200
        except KeyError:
            return None, 404

        asset["event"].append(data)
        asset.save()
        return None, 204







"""

Mock data

"""


@api.route('/event/')
@api.response(400, 'Event execution failed')
class Event(Resource):

    def get(self): 
        event = {
                "value": 123,
                "cid":  "xyz",
                "tid":  123,
                "name": "activate",
                "parameters": 
                    [
                        {
                            "name" : true
                        }
                    ]
            }

        return event, 200


@api.route('/threshold/')
@api.response(400, 'threshold execution failed')
class Event(Resource):

    def get(self): 
        value = 123

        return value, 200