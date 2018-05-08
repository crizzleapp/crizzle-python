import os
import time
import json
import logging
import requests
from abc import ABCMeta, abstractmethod
from crizzle.patterns import deprecated, assert_in

logger = logging.getLogger(__name__)


class Service(metaclass=ABCMeta):
    def __init__(self, name: str, root: str, key=None, default_api_version=None, debug=False):
        self.name = name
        self.root = root
        self.key_loaded = False
        self.api_key, self.secret_key = None, None
        self.default_api_version = default_api_version
        self.debug = debug
        self.load_key(key)
        logger.debug("Initialized {} environment".format(name))

    # region Helper methods
    @property
    def timestamp(self) -> int:
        """
        Truncated timestamp in milliseconds

        Returns:
            int: millisecond UNIX timestamp
        """
        return int(1000 * (time.time()))

    @property
    def nonce(self):
        """
        Returns a value that is always larger than the last

        Returns:
            int: millisecond timestamp (by default)
        """
        return int(time.time() * 1000)

    def get_default_params(self, **kwargs) -> dict:
        """
        Creates a dictionary of paramters to be sent by default along with every request

        Args:
            **kwargs: Keywork arguments that may be used to determine the default parameters

        Returns:
            dict: Default parameter dictionary
        """
        return {}

    def get_params(self, **kwargs) -> dict:
        """
        Get the final parameters to send with the request.

        Args:
            **kwargs: Keywork arguments that may be used to determine the default parameters

        Returns:
            dict: Dictionary containing the final parameters to be sent with the request
        """
        final_params = self.get_default_params(**kwargs)
        if 'params' in kwargs:
            params = kwargs['params']
            if params is not None:
                final_params.update(params)
        return final_params

    def load_key(self, key=None) -> None:
        """
        Loads the public and private API keys from a given file into self.api_key and self.secret_key.

        Args:
            key: Path to file containing API key and secret.
            The two keys must be on different lines, and the file must contain exactly 2 lines.

        Returns:
            tuple: (API key, Secret key)
        """
        if key is not None:
            if isinstance(key, str):
                with open(key, 'r') as file:
                    keys = json.load(file)
                    self.api_key, self.secret_key = keys['key'], keys['secret']
                self.key_loaded = True
            elif isinstance(key, dict):
                self.api_key, self.secret_key = key['key'], key['secret']
                self.key_loaded = True
        else:
            try:
                key = json.loads(os.environ['CrizzleKey_{}'.format(self.name)])
                self.load_key(key)
            except KeyError:
                logger.error('API key for service {} not found in environment variables.'.format(self.name))

    def json_number_hook(self, inp):
        if isinstance(inp, list):
            for k, v in enumerate(inp):
                # check values for integers
                if isinstance(v, (list, dict)):
                    inp[k] = self.json_number_hook(v)
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
                    inp[k] = self.json_number_hook(v)
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
    def sign_request_data(self, params=None, data=None, headers=None):
        """
        Sign the request with the secret key.

        Args:
            params:
            data:
            headers:

        Returns:

        """
        pass

    @abstractmethod
    def add_api_key(self, params=None, data=None, headers=None):
        """
        Adds API key to the request object.

        Args:
            data:
            headers:
            params:

        Returns:
            None
        """
        pass

    # endregion

    # region Request methods
    def request(self, request_type: str, endpoint: str, params=None, api_version=None, data=None, headers=None,
                sign=False):
        """
        Send a synchronous request to an API endpoint.

        Args:
            request_type (str): get | post | put | delete.
            endpoint (str): API endpoint to send the request to, for example: '24hticker'
            params (dict): Dictionary-like object containing the parameters to send with request
            api_version (str): API version to send the request to
            data (dict): Dictionary-like object containing the data to send with request
            headers (dict): Additional headers to send with the request
            sign (bool): whether or not to sign the request using the secret key

        Returns:

        """
        arguments = locals()
        if api_version is None:
            api_version = self.default_api_version
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        final_params = self.__class__.get_params(**arguments)

        # TODO: implement rate limiter

        with requests.Session() as session:
            try:
                assert_in(request_type, 'request_type', ('get', 'post', 'put', 'delete'))
            except ValueError:
                logger.exception('invalid request type {}'.format(request_type))
                raise
            else:
                if sign:
                    self.sign_request_data(params=final_params, data=data, headers=headers)
                self.add_api_key(params=final_params, data=data, headers=headers)
                request = requests.Request(request_type.upper(), self.root + "/{}/".format(api_version) + endpoint,
                                           params=final_params, data=data, headers=headers)
                prepped = request.prepare()
                response = session.send(prepped)
                try:
                    response.raise_for_status()
                except requests.HTTPError as e:
                    logger.exception("Error while querying endpoint '{}' of service '{}': '{}'".format(endpoint, self.name, response.text))
                finally:
                    logger.debug('Queried {} at {}'.format(self.name, response.url))
                    return response

    def get(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=False):
        return self.request('get', endpoint, params=params, api_version=api_version, data=data, headers=headers,
                            sign=sign)

    def post(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=True):
        return self.request('post', endpoint, params=params, api_version=api_version, data=data, headers=headers,
                            sign=sign)

    def put(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=True):
        return self.request('put', endpoint, params=params, api_version=api_version, data=data, headers=headers,
                            sign=sign)

    def delete(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=True):
        return self.request('delete', endpoint, params=params, api_version=api_version, data=data, headers=headers,
                            sign=sign)

    # endregion
