"""
Elastic API auth plugin for HTTPie.
"""

from httpie.plugins import AuthPlugin
from base64 import b64encode
import requests.auth

__version__ = '0.1.1'
__author__ = 'Derek Ditch'
__licence__ = 'MIT'


class ElasticAPIKeyAuth:
    def __init__(self, id: str, api_key: str):
        self.id = id
        self.api_key = api_key

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        """
        Override authorization serialization for "ApiKey" auth
        """
        request.headers['Authorization'] = type(self).make_header(
            self.id, self.api_key).encode('latin1')
        return request

    @staticmethod
    def make_header(id: str, api_key: str) -> str:
        credentials = u'%s:%s' % (id, api_key)
        token = b64encode(credentials.encode('utf8')).strip().decode('latin1')
        return 'ApiKey %s' % token


class ApiKeyPlugin(AuthPlugin):

    name = 'ApiKey auth'
    auth_type = 'apikey'
    description = 'Use Elastic ApiKey auth scheme'

    def get_auth(self, username, password) -> ElasticAPIKeyAuth:
        return ElasticAPIKeyAuth(id=username, api_key=password)
