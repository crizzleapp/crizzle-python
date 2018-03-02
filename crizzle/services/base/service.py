import time
import logging
import requests

logger = logging.getLogger(__name__)


class Service:
    # TODO: add postprocessing method
    # TODO: add instance-level switch to enable postprocessing in the request() method
    def __init__(self, name, root, key_file=None, default_api_version=None):
        self.name = name
        self.root = root
        self.key_loaded = False
        self.api_key, self.secret_key = None, None
        self.default_api_version = default_api_version
        if key_file is not None:
            self.load_key_file(key_file)
        logger.debug("Initialized {} environment".format(name))

    # region Helper methods
    @property
    def timestamp(self) -> int:
        return int(1000 * (time.time()))

    def get_default_params(self, **kwargs):
        return {}

    def get_final_params(self, **kwargs):
        final_params = self.get_default_params(**kwargs)
        if 'params' in kwargs:
            params = kwargs['params']
            if params is not None:
                final_params.update(params)
        return final_params

    @property
    def nonce(self):
        return int(time.time() * 1000)

    def load_key_file(self, key_file):
        if key_file is not None:
            with open(key_file, 'rb') as file:
                api_key = file.readline().strip()
                secret_key = file.readline().strip()
            self.key_loaded = True
            return api_key, secret_key
        else:
            return None, None

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

    def validate_arguments(self, method, *args, **kwargs):
        pass

    def add_api_key(self, request: requests.Request):
        request.headers['X-MBX-APIKEY'] = self.api_key

    def sign_request(self, request: requests.Request):
        pass
    # endregion

    # region Request methods
    def request(self, request_type: str, endpoint: str, params=None,
                api_version=None, data=None, headers=None, sign=False):
        arguments = locals()
        if api_version is None:
            api_version = self.default_api_version
        final_params = self.__class__.get_final_params(**arguments)
        logger.debug('Querying {}'.format(self.name))
        request = requests.Request(None, self.root + "/{}/".format(api_version) + endpoint,
                                   params=final_params, data=data, headers=headers)

        # TODO: implement rate limiter

        with requests.Session() as session:
            try:
                assert request_type in ('get', 'post', 'put', 'delete')
                request.method = request_type.upper()
            except AssertionError:
                logger.critical('invalid request type {}'.format(request_type))

            if sign:
                self.sign_request(request)
            self.add_api_key(request)
            prepped = request.prepare()
            response = session.send(prepped)
        return response


    def get(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=False):
        return self.request('get', endpoint, params=params, api_version=api_version,
                            data=data, headers=headers, sign=sign)

    def post(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=False):
        return self.request('post', endpoint, params=params, api_version=api_version,
                            data=data, headers=headers, sign=sign)

    def put(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=False):
        return self.request('put', endpoint, params=params, api_version=api_version,
                            data=data, headers=headers, sign=sign)

    def delete(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=False):
        return self.request('delete', endpoint, params=params, api_version=api_version,
                            data=data, headers=headers, sign=sign)

    # endregion
    pass


if __name__ == '__main__':
    print(Ellipsis)
