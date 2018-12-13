import os

from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

from app.endpoints import api


def create_app():
    app = Flask(__name__)
    api.init_app(app)
    return app


app = create_app()
app.app_context().push()
app.wsgi_app = ProxyFix(app.wsgi_app)