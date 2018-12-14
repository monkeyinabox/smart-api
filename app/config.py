# Flask settings
FLASK_DEBUG = True
FLASK_HOST = '0.0.0.0'

# Inventory
ASSETS_URL = 'http://dev.lupon.ch:5984'
ASSETS_USER = 'admin'
ASSETS_PASSWD = 'admin'
ASSETS_DB = 'assets'

# Things REST API
FOG_BASE_URL = 'http://localhost:5000'
INFLUX_BASE_URL = 'http://localhost:8086/query'
INFLUX_USER = ""
INFLUX_PASSWD = ""
INFLUX_DB = "telegraf"

# Controller 
CONTROLLER_URL = "http://isorp.ch:1880/events/"


OWM_URL = "https://api.openweathermap.org/data/2.5/"
OWM_APPID = "cd02c22f5d27d943433d755f8e253bf2"