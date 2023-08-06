import json
import os

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import urllib3
import certifi

from .rate_limiter import RateLimiter
from .resources import get_resource

__client = None


class __Client(object):
    BASE_URL = "https://api.stormglass.io/v2/"

    def __init__(self, encoding="utf8", api_key=None):
        self.rate_limit_lock = RateLimiter()
        self.encoding = encoding
        self.connection_pool = self._make_connection_pool()

        self._api_key = api_key or os.environ.get('STORMGLASS_API_KEY')

        if not self._api_key:
            raise ValueError('API key required')

    def _make_connection_pool(self):
        return urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

    def _compose_url(self, path, params=None):
        print(params)
        return f"{self.BASE_URL}{path}?{urlencode(params, True)}"

    def _handle_response(self, response):
        return json.loads(response.data.decode(self.encoding))

    def _request(self, method, path, params=None):
        url = self._compose_url(path, params)
        print(url)
        self.rate_limit_lock and self.rate_limit_lock.acquire()
        r = self.connection_pool.urlopen(method.upper(), url)

        return self._handle_response(r)

    def call(self, path, params):
        return self._request("GET", path, params=params)


def resource(name, config=None):
    global __client

    if not config:
        config = {}

    if not __client:
        __client = __Client(api_key=config.pop('api_key', None))

    return get_resource(name)(client=__client)
