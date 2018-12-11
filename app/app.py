""" 
import os
import ConfigParser
"""

from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

from endpoints import api

""" 
config = ConfigParser.ConfigParser()
config.read("settings.ini")
"""
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
