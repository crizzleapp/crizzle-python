import time
import logging
import time
import base
from time_handler import MONTH, check_valid_time_period

logger = logging.Logger(__name__)


class Environment(base.Environment):
    def query(self, url, data=None, params=None, headers=None, post=False):
        pass

    def __init__(self, key_file=None):
        super(Environment, self).__init__('poloniex', 'https://poloniex.com', key_file=key_file)
        self._nonce = int(time.time() * 1000)

    def query_public(self, method, data=None, params=None, headers=None):
        if params is None:
            params = {}
        url = self.uri + '/public'
        params['command'] = method
        return super(Environment, self).query_public(url, data=data, params=params, headers=headers)

    def query_private(self, method, data=None, params=None, headers=None):
        if params is None:
            params = {}
        url = self.uri + '/tradingApi'
        params['command'] = method
        return super(Environment, self).query_private(url, data=data, params=params, headers=headers)

    def parse_returned(self, returned):
        if 'error' in returned:
            raise Exception(returned['error'])
        else:
            return returned

    def hashify(self, url=None, data=None):
        return super().hashify(url=url, data=data)

    @property
    def nonce(self):
        """ Increments the nonce"""
        self._nonce += 42
        return self._nonce

    def get_all_positions(self) -> list:
        pass

    def place_order(self):
        pass

    def get_current_rate(self, pair: str):
        pass
