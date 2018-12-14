from flask_restplus import Namespace, Resource, fields
from cloudant.client import CouchDB
from flask import request
from app import config

from app.endpoints.assets import assets, assets_location

api = Namespace('Widgets', description='Widget managmenet operations')

widgets_config = api.model('config', {
        'key': fields.String(descripton="configuration key"),
        'value': fields.String(descripton="configuration value")
})

widgets = api.model('widget', {
        '_id': fields.String(descripton="widget ID"),
        'name': fields.String(descripton="name"),
        'assets': fields.List(fields.Nested(assets)),
        'config': fields.List(fields.Nested(widgets_config))
})

try:
    client = CouchDB(config.ASSETS_USER, config.ASSETS_PASSWD, url=config.ASSETS_URL, connect=True)
    session = client.session()
    mydb = client[config.WIDGETS_DB]
except:
    print("No DB Connection possible")

@api.route('/')
@api.response(404, 'Widget not found.')
class MapList(Resource):

    @api.marshal_with(widgets)
    def get(self):
        """
        Returns a list of all widgets.
        """
        data = []
        for document in mydb:
            data.append(document)
        return data
    
    @api.expect(widgets)
    @api.response(204, 'New Widget created sucessfully')
    @api.response(302, 'Widget id already exists')
    def post(self):
        """
        Create new Widget
        """
        data = request.json
        
        tmp_doc = data['_id'] in mydb
        if tmp_doc:
            return 302
        
        mydb.create_document(data)
        return None, 204