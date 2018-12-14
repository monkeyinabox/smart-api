from flask_restplus import Namespace, Resource, fields
from flask import request
import requests
from app import config

api = Namespace('OpenWeatherMap', description='Get current wather codition from OpenWeatherMap')

headers = { 
    'cache-control': "no-cache" 
}

@api.route('/weather')
@api.response(400, 'API call failed')
@api.response(200, 'Success')
@api.response(500, 'OWM not reachable')
class OwmWeather(Resource):
    def get(self):
        """
        Current weather data
        """
        querystring = { "id":"7285241", # Citiy ID of Biel/Bienne 
                        "units":"metric",
                        "APPID": config.OWM_APPID}
        response = requests.request("GET", config.OWM_URL+"weather", headers=headers, params=querystring, verify=False)
        if not response.ok:
            return None, 400
        else:
            return response.json(), 200


@api.route('/forecast')
@api.response(400, 'API call failed')
@api.response(200, 'Success')
@api.response(500, 'OWM not reachable')
class OwmForecast(Resource):
    def get(self):
        """
        5 day weather forecast
        """
        querystring = { "id":"7285241", # Citiy ID of Biel/Bienne 
                        "units":"metric",
                        "APPID": config.OWM_APPID}
        response = requests.request("GET", config.OWM_URL+"forecast", headers=headers, params=querystring, verify=False)
        if not response.ok:
            return None, 400
        else:
            return response.json(), 200