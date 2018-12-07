"""API configuration.

.. moduleauthor:: Mobile App Team
"""

import os


class FlaskConfig(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')


class DevelopmentConfig(FlaskConfig):
    """Configurations for Development."""
    DEBUG = True
    SECRET_KEY = 'admin'


class ProductionConfig(FlaskConfig):
    """Configuration for production, extends FlaskConfig"""


class TestingConfig(FlaskConfig):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True


flask_config_type = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
