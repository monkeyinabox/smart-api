#!flask/bin/python
# 
import logging
from app import app
from flask_cors import CORS

logging.basicConfig(level=logging.DEBUG)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.run(debug=True,host='0.0.0.0')



