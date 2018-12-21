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


@api.route('/<widget_id>/')
@api.response(404, 'Widget not found.')
class MapWidgetById(Resource):

    @api.marshal_with(widgets)
    def get(self, widget_id):
        """
        Returns a list of all widgets.
        """
        try:
            if mydb[widget_id]:
                return mydb[widget_id], 200
        except KeyError:
            return None, 404


@api.route('/<widget_id>/config/')
@api.response(404, 'Config not found.')
class MapConfigByWidget(Resource):

    @api.marshal_with(widgets_config)
    def get(self, widget_id):
        """
        Returns a list of all widgets.
        """
        try:
            if mydb[widget_id]:
                return mydb[widget_id]["config"], 200
        except KeyError:
            return None, 404
    

    @api.expect(widgets_config)
    @api.response(204, 'New Config created sucessfully')
    #@api.response(302, 'Widget id already exists')
    def post(self, widget_id):
        """
        Create new config
        """
        data = request.json
        widget = None
        try:
            if mydb[widget_id]:
                widget = mydb[widget_id], 200
        except KeyError:
            return None, 404
        config = widget[0]["config"]
        config.append(data)
        mydb[widget_id].save()
        return None, 204

