#!venv/bin/python

import os
import logging
import json
import db

from util.helper import populate_db
from api.app import flask_app
from api.config import flask_config_type
from logging.config import fileConfig



logger = logging.getLogger(__name__)

flask_app.config.from_object(flask_config_type["production"])

# Found on https://stackoverflow.com/a/7166139
cur_path = os.path.dirname(os.path.realpath(__file__))
rel_path = "util/logging.json"
json_config_path = os.path.join(cur_path, rel_path)

logger.log(20, "Loading logging config from json-file")
with open(json_config_path, "r", encoding="utf-8") as logging_config:
    logging.config.dictConfig(json.load(logging_config))
    # source of "logging.json": https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/

logger.log(20, "Connecting to or starting database")
db.run_database(db.dbConfigType["memory"])
populate_db()

if __name__ == "__main__":
    logger.log(20, "Staring Flask application")
    flask_app.run()

