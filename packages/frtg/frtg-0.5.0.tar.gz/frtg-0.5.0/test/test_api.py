import json
import os
import tempfile

import jsonschema
import pytest

import frtg

DEFAULT_REQUEST_HEADERS = {
    'Content-type': 'application/json',
    'Accept': ['application/json']
}

TWEET_LIST_RESPONSE_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-07/schema#',

    'definitions': {
        'time': {'type': 'string'},
        'user-info': {
            'properties': {
                'name': {'type': 'string'},
                'screen_name': {'type': 'string'},
                'profile_image': {'type': 'string'},
                'user_loc': {'type': 'string'}
            },
            'required': ['name', 'screen_name', 'profile_image', 'user_loc'],
            'additionalProperties': False
        },
        'retweet-info': {
            'properties': {
                'time': {'$ref': '#/definitions/time'},
                'user': {'$ref': '#/definitions/user-info'}
            },
            'required': ['time', 'user'],
            'additionalProperties': False
        },
        'tweet-info': {
            'type': 'object',
            'properties': {
                'time': {'$ref': '#/definitions/time'},
                'user': {'$ref': '#/definitions/user-info'},
                'hashtags': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
                'text': {'type': 'string'},
                'html': {'type': 'string'},
                'retweet': {'$ref': '#/definitions/retweet-info'}
            },
            'required': ['time', 'user', 'hashtags', 'text', 'html'],
            'additionalProperties': False
        }
    },

    'type': 'array',
    'items': {'$ref': '#/definitions/tweet-info'}
}


@pytest.fixture
def config_file():
    params = {
        'credentials': {
            'consumer key': 'zzzzzzzzzzzzz',
            'consumer secret': 'zzzzzzzzzzzzz'
        },
        'search': {
            'filter hints': ['aaa', 'bbb', 'ccc'],
            'max nr rows': 999
        }
    }

    with tempfile.NamedTemporaryFile() as f:
        f.write(json.dumps(params).encode('utf-8'))
        f.flush()
        yield f.name


@pytest.fixture
def client(config_file):
    os.environ['CONFIG_FILENAME'] = config_file
    with frtg.create_app().test_client() as c:
        yield c


class MockedTwython:

    SAMPLE_DATA_FILENAME = os.path.join(
        os.path.dirname(__file__),
        'sample_query_response.json')

    def __init__(self, *args, **kwargs):
        pass

    def search(self, **kwargs):
        # some sanity checks on the expected search args
        for varname in ['q', 'count', 'tweet_mode']:
            assert varname in kwargs.keys()
        assert kwargs['tweet_mode'] == 'extended'

        with open(MockedTwython.SAMPLE_DATA_FILENAME) as f:
            return {'statuses': json.loads(f.read())}


def test_tweet_list(client, mocker):

    mocker.patch('frtg.routes.Twython', MockedTwython)

    rv = client.get('/tweets', headers=DEFAULT_REQUEST_HEADERS)
    assert rv.status_code == 200
    assert rv.is_json
    response_data = json.loads(rv.data.decode('utf-8'))
    jsonschema.validate(response_data, TWEET_LIST_RESPONSE_SCHEMA)
    assert len(response_data) > 0, \
        'sanity check: expected a non-empty response'
