import logging
from urllib.parse import urlencode
from http.client import HTTPException
import requests
import time
import hmac
from base64 import b64decode, b64encode
from hashlib import sha256, sha512

logger = logging.getLogger(__name__)


class ParentAPI:
    def __init__(self, name, uri, key_file=None):
        self.key, self.secret = None, None
        self.key_loaded = False
        if key_file is not None:
            self.load_api_key(key_file)

        self.name = name
        self.uri = uri
        self._nonce = int(time.time() * 1000)

    @property
    def nonce(self):
        self._nonce += 42
        return self._nonce

    def _json_number_hook(self, json_dict):
        if isinstance(json_dict, list):
            for k, v in enumerate(json_dict):
                try:
                    json_dict[k] = float(v)
                except (ValueError, TypeError):
                    pass
        else:
            for k, v in json_dict.items():
                # check values for integers
                if isinstance(v, (list, dict)):
                    json_dict[k] = self._json_number_hook(v)
                else:
                    try:
                        json_dict[k] = float(v)
                    except (ValueError, TypeError):
                        pass

                # check keys for integers
                try:
                    json_dict[float(k)] = json_dict[k]
                    del json_dict[k]
                except ValueError:
                    pass
        return json_dict

    def query(self, url, data=None, params=None, headers=None, post=False):
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        if params is None:
            params = {}
        # print('QUERYING: {}'.format(self.name))
        # print('DATA: {}'.format(data))
        # print('HEADERS: {}'.format(headers))
        logger.info('Querying {}'.format(self.name))
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
        return self.parse_returned(ret.json(object_hook=self._json_number_hook))

    def query_public(self, url, data=None, params=None, headers=None):
        """

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

    def hashify(self, url=None, data=None):
        data['nonce'] = self.nonce
        post_data = urlencode(data)

        # Encode unicode objects before hashing
        encoded = (str(data['nonce']) + post_data).encode()
        message = url.encode() + sha256(encoded).digest()
        signature = hmac.new(b64decode(self.secret), message, sha512)
        sigdigest = b64encode(signature.digest())

        data.update({'API-Key': self.key, 'API-Sign': sigdigest.decode()})
        print('HASHIFY OUTPUT: {}'.format(data))
        return data

    def load_api_key(self, key_file):
        with open(key_file, 'r') as f:
            lines = f.readlines()
            try:
                assert len(lines) == 2
                self.key, self.secret = [line.strip() for line in lines]
                self.key_loaded = True
            except AssertionError as e:
                print('Key file must have key and secret on exactly two lines, instead has {}'.format(len(lines)))
                raise e

    def rate(self, target):
        pass

    def parse_returned(self, returned):
        logger.debug('PARSING {}'.format(returned))
        return returned


if __name__ == '__main__':
    test = ParentAPI('name', 'https://api.kraken.com')
