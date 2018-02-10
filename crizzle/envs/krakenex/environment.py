import logging
from crizzle.envs import base

logger = logging.getLogger(__name__)


class Environment(base.Environment):
    def __init__(self, key_file=None):
        super(Environment, self).__init__('kraken', 'https://api.kraken.com', key_file=key_file)
        self.api_version = '0'

    def query(self, url, data=None, params=None, headers=None, post=False):
        super().query(url, data=data, params=params, headers=headers, post=False)

    def query_public(self, method, data=None, params=None, headers=None):
        logger.debug('METHOD: {}'.format(method))
        url = self._uri + '/' + self.api_version + '/public/' + method
        return super(Environment, self).query_public(url, data=data, params=params, headers=headers)

    def query_private(self, method, data=None, params=None, headers=None):
        url = self._uri + '/' + self.api_version + '/private/' + method
        return super(Environment, self).query_private(url, data=data, params=params, headers=headers)
    
    def hashify(self, url=None, data=None):
        super().hashify(url, data=data)

    def parse_returned(self, returned):
        if returned['error']:
            raise Exception(returned['error'])
        else:
            return super(Environment, self).parse_returned(returned['result'])

    def get_positions(self) -> list:
        pass

    def get_current_rate(self, pair: str):
        pass

