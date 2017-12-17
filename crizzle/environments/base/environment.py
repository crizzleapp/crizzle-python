import hmac
import logging
import time
from abc import ABC, abstractmethod
from base64 import b64decode, b64encode
from hashlib import sha256, sha512
from http.client import HTTPException
from urllib.parse import urlencode

import requests

from crizzle.agent import Agent
from crizzle.environments.base.agentInterface import Space, Action, Observation
from crizzle.singleton import Singleton

logger = logging.getLogger(__name__)


class Environment(ABC, metaclass=Singleton):
    _action_space = None
    _observation_space = None

    def __init__(self, name, uri, key_file=None):
        self._key, self.secret = None, None
        self._key_loaded = False
        if key_file is not None:
            self.load_api_key(key_file)
        self._name = name
        self._uri = uri
        self._nonce = int(time.time() * 1000)
        self._info = {}
        self._agents = []
        self._observation = Observation()
        logger.debug("Initialized {} environment".format(name))

    # region basic API methods

    @property
    def nonce(self):
        self._nonce += 64
        return self._nonce

    def _json_number_hook(self, inp):
        if isinstance(inp, list):
            for k, v in enumerate(inp):
                # check values for integers
                if isinstance(v, (list, dict)):
                    inp[k] = self._json_number_hook(v)
                else:
                    try:
                        f = float(v)
                        if f.is_integer():
                            f = int(f)
                        inp[k] = f
                    except (ValueError, TypeError):
                        pass
        elif isinstance(inp, dict):
            for k, v in inp.items():
                # check values for integers
                if isinstance(v, (list, dict)):
                    inp[k] = self._json_number_hook(v)
                else:
                    try:
                        f = float(v)
                        if f.is_integer():
                            f = int(f)
                        inp[k] = f
                    except (ValueError, TypeError):
                        pass
        return inp

    def query(self, url, data=None, params=None, headers=None, post=False):
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        if params is None:
            params = {}
        logger.debug('Querying {}'.format(self._name))
        logger.debug('DATA: {}'.format(data))
        logger.debug('HEADERS: {}'.format(headers))
        if post:
            ret = requests.post(url, data=data, params=params, headers=headers)
        else:
            ret = requests.get(url, data=data, params=params, headers=headers)
        logger.debug('URL: {}'.format(ret.url))

        status = ret.status_code
        try:
            assert status in (200, 201, 202)
        except AssertionError:
            logger.error('Error while querying {}'.format(ret.url))
            raise HTTPException(status)
        ret = self.parse_returned(ret.json(object_hook=self._json_number_hook))
        logger.debug(ret)
        return ret

    def query_public(self, url, data=None, params=None, headers=None):
        """

        :param params:
        :param url: The full request URL
        :param data:
        :param headers:
        :return:
        """
        if data is None:
            data = {}

        return self.query(url, data=data, params=params, headers=headers, post=False)

    def query_private(self, url, data=None, params=None, headers=None):
        """

        :param params:
        :param url: The full request URL
        :param data:
        :param headers:
        :return:
        """
        if data is None:
            data = {}
        if headers is None:
            headers = {}
        assert self._key_loaded

        h, d = self.hashify(url, data)
        data.update(d)
        headers.update(h)

        return self.query(url, data=data, params=params, headers=headers, post=True)

    def hashify(self, url=None, data=None):
        data['nonce'] = self.nonce
        post_data = urlencode(data)

        # Encode unicode objects before hashing
        encoded = (str(data['nonce']) + post_data).encode()
        message = url.encode() + sha256(encoded).digest()
        signature = hmac.new(b64decode(self.secret), message, sha512)
        sigdigest = b64encode(signature.digest())

        data.update({'API-Key': self._key, 'API-Sign': sigdigest.decode()})
        logger.debug('HASHIFY OUTPUT: {}'.format(data))
        return data

    def load_api_key(self, key_file):
        with open(key_file, 'r') as f:
            lines = f.readlines()
            try:
                assert len(lines) == 2
                self._key, self.secret = [line.strip() for line in lines]
                self._key_loaded = True
            except AssertionError as e:
                logger.fatal(
                    'Key file must have key and secret on exactly two lines, instead has {}'.format(len(lines)))
                raise e

    def get_data(self, data_sources: dict):
        """
        Return data from all available sources: rates, tweets, etc.

        Returns:
            A dictionary of all available data sources
        """
        for source in data_sources.values():
            data = source.get_data()

    # endregion

    # region gym-like methods

    @property
    @abstractmethod
    def agents(self):
        """
        Agents registered with environment

        Returns:
            (list) List of agents registered with environment
        """
        return self._agents

    @abstractmethod
    def add_agent(self, agent: Agent) -> None:
        """
        Add agent to registered agents

        Args:
            agent (Agent):

        Returns:
            None
        """
        self._agents.append(agent)
        logger.debug("Added agent {} to environment {}".format(agent, self._name))

    @abstractmethod
    def buy(self, pair: str, rate: float, amount: float):
        """
        place a buy order for a currency pair

        Args:
            pair (str): currency pair ('BTC_ETH', for example)
            rate (float): rate at which to place order
            amount (float): how much of the currency to order

        Returns:
            None
        """
        pass

    @abstractmethod
    def cancel(self, *args, **kwargs):
        """
        Cancel an order that has already been placed

        Args:
            *args:
            **kwargs:

        Returns:

        """

    @abstractmethod
    def sell(self, pair: str, rate: float, amount: float):
        """
        place a buy order for a currency pair

        Args:
            pair (str): currency pair ('BTC_ETH', for example)
            rate (float): rate at which to place order
            amount (float): how much of the currency to order

        Returns:
            None
        """

    @property
    @abstractmethod
    def action_space(self) -> Space:
        """
        All the actions possible in the environment

        Returns:
            A list of all actions possible in the environment
        """
        return self.__class__._action_space

    @property
    @abstractmethod
    def observation_space(self) -> Space:
        return self.__class__._observation_space

    @property
    @abstractmethod
    def info(self) -> dict:
        """
        Debug information for agents

        Returns:
            (dict) any extra information not provided in the observation
        """
        return self._info

    @property
    @abstractmethod
    def observation(self) -> Observation:
        """
        The current observation

        Returns:
            (Observation)
        """
        return self._observation

    @abstractmethod
    def step(self, action: Action) -> Observation:
        """
        Perform action and return observation

        Args:
            action (Action):

        Returns:
            Observation: observation after performing action
        """
        return self._observation

    @property
    @abstractmethod
    def done(self):
        pass

    @abstractmethod
    def reset(self) -> Observation:
        return Observation()

    @abstractmethod
    def render(self) -> None:
        pass

    # endregion

    @abstractmethod
    def parse_returned(self, returned):
        return returned

    @abstractmethod
    def get_historical_data(self, pair: str, interval: int):
        pass

    @abstractmethod
    def get_current_rate(self, pair: str):
        """
        Get the current exchange rate given a cu

        Args:
            pair:

        Returns:

        """
        pass

    @abstractmethod
    def get_positions(self) -> list:
        """
        Get current positions

        Returns:
            A list of all currently held positions
        """
        pass


if __name__ == '__main__':
    print(Ellipsis)