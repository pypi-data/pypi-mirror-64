"""
automatically invoked app factory
"""
import json
import logging
import os

from flask import Flask
import jsonschema

logger = logging.getLogger(__name__)
CONFIG_ENV_VAR_NAME = 'CONFIG_FILENAME'


CONFIG_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'credentials': {
            'type': 'object',
            'properties': {
                'consumer key': {'type': 'string'},
                'consumer secret': {'type': 'string'},
                'access token key': {'type': 'string'},
                'access token secret': {'type': 'string'},
            },
            'required': ['consumer key', 'consumer secret'],
            'additionalProperties': False
        },
        'search': {
            'type': 'object',
            'properties': {
                'filter hints': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
                'max nr rows': {'type': 'integer'}
            },
            'required': ['filter hints', 'max nr rows'],
            'additionalProperties': False
        }
    },
    'required': ['credentials', 'search'],
    'additionalProperties': False
}


def create_app():
    """
    :return: a new flask app instance
    """

    assert CONFIG_ENV_VAR_NAME in os.environ, \
        'expected {} to be defined in the environment'.format(
            CONFIG_ENV_VAR_NAME)
    config_filename = os.environ[CONFIG_ENV_VAR_NAME]
    assert os.path.isfile(config_filename), \
        'config file {} not found'.format(config_filename)

    with open(config_filename) as f:
        config = json.loads(f.read())
        jsonschema.validate(config, CONFIG_SCHEMA)

    app = Flask(__name__)
    app.secret_key = 'super secret session key'
    app.config['TWITTER_PARAMS'] = config

    from frtg import routes
    app.register_blueprint(routes.blueprint, url_prefix='/')

    logger.info('frtg Flask app initialized')

    return app
