import time
import logging
import time
from crizzle.environments import base
from crizzle.environments.time_handler import MONTH, check_valid_time_period

logger = logging.Logger(__name__)


class Environment(base.Environment):
    """
    Environment for the Poloniex exchange
    """
    _observation_space = base.Bounded(-1, 1)
    _action_space = base.Bounded(-1, 1)
    def __init__(self, key_file=None):
        super(Environment, self).__init__('poloniex', 'https://poloniex.com', key_file=key_file)
        self._nonce = int(time.time() * 1000)
        self._info = {}
        self._observation = base.Observation()

    @property
    def info(self) -> dict:
        return self._info

    @property
    def observation(self) -> base.Observation:
        return self._observation

    @property
    def observation_space(self) -> base.Space:
        return Environment._observation_space

    @property
    def action_space(self) -> base.Space:
        return Environment._action_space

    def render(self) -> None:
        pass

    def step(self, action: base.Action) -> base.Observation:
        pass

    def reset(self) -> base.Observation:
        pass

    def query(self, url, data=None, params=None, headers=None, post=False):
        pass

    def query_public(self, method, data=None, params=None, headers=None):
        if params is None:
            params = {}
        url = self._uri + '/public'
        params['command'] = method
        return super(Environment, self).query_public(url, data=data, params=params, headers=headers)

    def query_private(self, method, data=None, params=None, headers=None):
        if params is None:
            params = {}
        url = self._uri + '/tradingApi'
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

    def get_positions(self) -> list:
        pass

    def get_current_rate(self, pair: str):
        pass

    def get_historical_data(self, pair: str, interval: int):
        pass
