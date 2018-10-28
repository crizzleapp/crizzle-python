import os
import time
import json
import logging
import requests
from collections import OrderedDict
from abc import ABCMeta
from crizzle.utils import assert_in

logger = logging.getLogger(__name__)


class Service(metaclass=ABCMeta):
    def __init__(self, name: str, root: str, key=None, default_api_version=None,
                 debug=False, default_timestamp=None):
        """

        Args:
            name:
            root:
            key:
            default_api_version:
            debug:
        """
        self.name = name
        self.root = root
        self.default_api_version = default_api_version
        self.debug = debug
        self.default_timestamp = default_timestamp
        self.load_key(key)
        self.session = requests.Session()
        logger.debug("Initialized {} environment".format(name))

    # region Helper methods
    @property
    def key(self):
        return None

    @property
    def key_loaded(self):
        return self.key is not None

    def load_key(self, key) -> None:
        """
        Check if key is in env variables, else load from file or dict.

        Args:
            key (str/dict): File or dict to load key from

        Returns:
            None
        """
        # TODO: is using env variables to store keys secure?
        env_variable_name = 'CrizzleKey_{}'.format(self.name)
        if key is None:
            if env_variable_name not in os.environ:
                logger.warning("API key for service '{}' not found in environment variables. "
                               "Functionality will be limited. "
                               "Use `svc.load_key(dict_or_filepath)` to load a key".format(self.name))
        else:
            if isinstance(key, str):  # assume key is a file path (str)
                try:
                    with open(key) as file:
                        os.environ[env_variable_name] = file.read()
                except FileNotFoundError:
                    logger.error(
                        "Could not find file at {}. When running on a remote machine, this is not an error.".format(
                            key))
            elif isinstance(key, dict):  # assume key is a dict
                try:
                    os.environ[env_variable_name] = json.dumps(key)
                except json.JSONDecodeError:
                    logger.error('Could not parse contents of key dict.')

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
            **kwargs: Keyword arguments used to determine the default parameters

        Returns:
            dict: Default parameter dictionary
        """
        return kwargs

    def get_params(self, **kwargs) -> dict:
        """
        Get the final parameters to send with the request.

        Args:
            **kwargs: Keyword arguments that may be used to determine the default parameters

        Returns:
            dict: Dictionary containing the final parameters to be sent with the request
        """
        final_params = self.get_default_params(**kwargs)
        if 'params' in kwargs:
            params = kwargs['params']
            if params is not None:
                final_params.update(params)
        return final_params

    @staticmethod
    def sort_dict(dictionary: dict):
        sorted_keys = sorted(dictionary.keys())
        return OrderedDict([(key, dictionary[key]) for key in sorted_keys])

    def sign_request_data(self, params=None, data=None, headers=None):
        """
        Sign the request params/data/headers with the secret key in accordance with the API spec.

        Args:
            params (dict): request params
            data (dict): request data
            headers (dict): request headers

        Returns:

        """
        return {'params': params, 'data': data, 'headers': headers}

    def add_api_key(self, params=None, data=None, headers=None):
        """
        Adds API key to the request params/data/headers in accordance with the API spec.

        Args:
            params (dict): request params
            data (dict): request data
            headers (dict): request headers

        Returns:
            None
        """
        return {'params': params, 'data': data, 'headers': headers}

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

    # endregion

    # region Request methods
    def request(self, request_type: str, endpoint: str, params=None, api_version=None, data=None, headers=None,
                sign=False, add_api_key=True):
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
            add_api_key:

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
        headers = self.sort_dict(headers)
        final_params = self.sort_dict(final_params)
        data = self.sort_dict(data)

        with self.session as session:
            try:
                assert_in(request_type, 'request_type', ('get', 'post', 'put', 'delete'))
            except ValueError:
                logger.exception('invalid request type {}'.format(request_type))
                raise
            else:
                if sign:
                    self.sign_request_data(params=final_params, data=data, headers=headers)
                if add_api_key:
                    self.add_api_key(params=final_params, data=data, headers=headers)
                request = requests.Request(request_type.upper(), self.root + "/{}/".format(api_version) + endpoint,
                                           params=final_params, data=data, headers=headers)
                prepped = request.prepare()
                if self.debug:
                    return prepped
                else:
                    response = session.send(prepped)
                    try:
                        response.raise_for_status()
                    except requests.HTTPError as e:
                        logger.exception(
                            "Error while querying endpoint '{}' of service '{}': '{}'".format(endpoint, self.name,
                                                                                              response.text))
                    finally:
                        logger.debug('Queried {} at {}'.format(self.name, response.url))
                        return response

    def get(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=False, add_api_key=True):
        return self.request('get', endpoint, params=params, api_version=api_version, data=data, headers=headers,
                            sign=sign, add_api_key=add_api_key)

    def post(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=True, add_api_key=True):
        return self.request('post', endpoint, params=params, api_version=api_version, data=data, headers=headers,
                            sign=sign, add_api_key=add_api_key)

    def put(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=True, add_api_key=True):
        return self.request('put', endpoint, params=params, api_version=api_version, data=data, headers=headers,
                            sign=sign, add_api_key=add_api_key)

    def delete(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=True,
               add_api_key=True):
        return self.request('delete', endpoint, params=params, api_version=api_version, data=data, headers=headers,
                            sign=sign, add_api_key=add_api_key)

    # endregion
