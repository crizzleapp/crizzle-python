import logging
from abc import ABC, abstractmethod
# noinspection PyCompatibility
from urllib.parse import urlencode
# noinspection PyCompatibility
from http.client import HTTPException
import requests
import time
import hmac
from base64 import b64decode, b64encode
from hashlib import sha256, sha512
from singleton import Singleton

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Environment(ABC, metaclass=Singleton):
    def __init__(self, name, uri, key_file=None):
        self.key, self.secret = None, None
        self.key_loaded = False
        if key_file is not None:
            self.load_api_key(key_file)
        self.name = name
        self.uri = uri
        self._nonce = int(time.time() * 1000)
        logger.debug("Initialized {} environment".format(name))

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

    @abstractmethod
    def query(self, url, data=None, params=None, headers=None, post=False):
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        if params is None:
            params = {}
        logger.debug('Querying {}'.format(self.name))
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

    @abstractmethod
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

    @abstractmethod
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
        assert self.key_loaded

        h, d = self.hashify(url, data)
        data.update(d)
        headers.update(h)

        return self.query(url, data=data, params=params, headers=headers, post=True)

    @abstractmethod
    def hashify(self, url=None, data=None):
        data['nonce'] = self.nonce
        post_data = urlencode(data)

        # Encode unicode objects before hashing
        encoded = (str(data['nonce']) + post_data).encode()
        message = url.encode() + sha256(encoded).digest()
        signature = hmac.new(b64decode(self.secret), message, sha512)
        sigdigest = b64encode(signature.digest())

        data.update({'API-Key': self.key, 'API-Sign': sigdigest.decode()})
        logger.debug('HASHIFY OUTPUT: {}'.format(data))
        return data

    def load_api_key(self, key_file):
        with open(key_file, 'r') as f:
            lines = f.readlines()
            try:
                assert len(lines) == 2
                self.key, self.secret = [line.strip() for line in lines]
                self.key_loaded = True
            except AssertionError as e:
                logger.fatal('Key file must have key and secret on exactly two lines, instead has {}'.format(len(lines)))
                raise e

    @abstractmethod
    def parse_returned(self, returned):
        logger.debug('PARSING {}'.format(returned))
        return returned

    def get_data(self, data_sources: dict):
        """
        Return data from all available sources: rates, tweets, etc.
        :param data_sources:
        :return: A dictionary of all available data sources
        """
        for source in data_sources.values():
            data = source.get_data()
            pass

    @abstractmethod
    def get_historical_prices(self, pair: str, interval: int):
        pass

    @abstractmethod
    def place_order(self):
        pass

    @abstractmethod
    def get_current_rate(self, pair: str):
        pass

    @abstractmethod
    def get_all_positions(self) -> list:
        pass


if __name__ == '__main__':
    test = Environment('name', 'https://api.kraken.com')
