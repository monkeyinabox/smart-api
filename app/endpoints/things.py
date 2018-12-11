from flask_restplus import Namespace, Resource, fields
from flask import request
import requests

api = Namespace('Things', description='things related operations')

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


FOG_BASE_URL = 'http://localhost:5000'

@api.route('/')
@api.response(404, 'Category not found.')
class Thinglist(Resource):
    @api.doc('list_things')
    @api.marshal_with(thing_list)
    def get(self):
        """
        Returns a list of all things
        """
        response = requests.get(FOG_BASE_URL + "/things")
        if not response.ok:
            return None, response.status_code
        else:
            print(response.content)
            return response.json(), response.status_code
    

@api.route('/<id>')
@api.response(404, 'thing not found.')
class ThingItem(Resource):

    @api.marshal_with(thing)
    def get(self, id):
        """
        Returns thing description
        """
        response = requests.get(FOG_BASE_URL + "/things/" + id)
        if not response.ok:
            return None, response.status_code
        else:
            print(response.content)
            return response.json(), response.status_code



"""
Calling InfluxDB to get last known value of a sensor
"""
INFLUX_BASE_URL = 'http://localhost:8086/query'
headers = { 
    'cache-control': "no-cache" 
}
INFLUX_USER = ""
INFLUX_PASSWD = ""


@api.route('/<id>/<name>')
@api.response(404, 'thing or sensor not found.')
@api.response(500, 'InfluxDB connection refused')
class ThingItemValue(Resource):

    def get(self, id, name):
        """
        Returns last recorded data value, Note: return values does not indicate if query provided a valid output!
        """
        querystring = {"db":"telegraf",
                       "p": INFLUX_USER,
                       "u": INFLUX_PASSWD,
                       "q":"SELECT last(\"{}\") FROM \"autogen\".\"mqtt_consumer\" WHERE \"topic\"=\'nexhome/data/{}/{}\'".format(name, id, name)}
        response = requests.request("GET", INFLUX_BASE_URL, headers=headers, params=querystring, verify=False)
        return response.json(), response.status_code
