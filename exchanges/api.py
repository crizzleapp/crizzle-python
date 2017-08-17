from urllib.parse import urlencode
from http.client import HTTPException
import logging
import requests
import time
import hmac
from hashlib import sha256, sha512
from base64 import b64decode, b64encode


class ParentAPI:
    def __init__(self, name, uri, key_file=None):
        self.key_loaded = False
        if key_file is not None:
            self.load_api_key(key_file)

        self.name = name
        self.uri = uri

    def query(self, url, data, headers=None):
        if headers is None:
            headers = {}

        ret = requests.get(url, params=data, headers=headers)
        logging.debug('querying {}'.format(ret.url))
        try:
            status = ret.status_code
            assert status in (200, 201, 202)
        except AssertionError:
            logging.error('Error while querying {}'.format(ret.url))
            raise HTTPException(status)
        return self.parse_returned(ret.json())

    def query_public(self, method, data=None):
        url_path = '/public/' + method

        if data is None:
            data = {}

        return self.query(url_path, data)

    def query_private(self, method, data=None):
        if data is None:
            data = {}
        assert self.key_loaded

        url_path = '/private/' + method
        data['nonce'] = int(1000 * time.time())
        post_data = urlencode(data)

        # Encode unicode objects before hashing
        encoded = (str(data['nonce']) + post_data).encode()
        message = url_path.encode() + sha256(encoded).digest()
        signature = hmac.new(b64decode(self.secret), message, sha512)
        sigdigest = b64encode(signature.digest())

        headers = {'API-Key': self.key,
                   'API-Sign': sigdigest.decode()}

        return self.query(url_path, data, headers)

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
        if returned['error']:
            raise Exception(returned['error'])
        else:
            return returned['result']
