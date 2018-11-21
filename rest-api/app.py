
import logging

from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

from endpoints import api

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api.init_app(app)


#logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
#logging.config.fileConfig(logging_conf_path)
#log = logging.getLogger(__name__)

app.run(debug=True)