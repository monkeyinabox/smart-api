#!flask/bin/python
# 
import logging
from app import app

logging.basicConfig(level=logging.DEBUG)

app.run(debug=True,host='0.0.0.0')


