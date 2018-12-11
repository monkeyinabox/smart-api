from flask_restplus import Namespace, Resource, fields
from flask import request
import requests

api = Namespace('OpenWeatherMap', description='Get current wather codition from OpenWeatherMap')


OWM_URL = "https://api.openweathermap.org/data/2.5/"
APPID = "cd02c22f5d27d943433d755f8e253bf2"
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
                        "APPID": APPID}
        response = requests.request("GET", OWM_URL+"weather", headers=headers, params=querystring, verify=False)
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
                        "APPID": APPID}
        response = requests.request("GET", OWM_URL+"forecast", headers=headers, params=querystring, verify=False)
        if not response.ok:
            return None, 400
        else:
            return response.json(), 200