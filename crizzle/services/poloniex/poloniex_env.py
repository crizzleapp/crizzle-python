import time
import logging
import requests
from crizzle.services.base import Service as BaseService

logger = logging.Logger(__name__)


class Service(BaseService):
    """
    Environment for the Poloniex exchange
    """
    def __init__(self, key_file=None):
        super(Service, self).__init__('Poloniex', 'https://poloniex.com/', key_file=key_file)

    # region Request methods
    def request(self, request_type: str, endpoint: str, params=None,
                api_version=None, data=None, headers=None, sign=False):
        final_params = self.get_params()
        if params is not None:
            final_params.update(params)
        logger.debug('Querying {}'.format(self.name))
        request = requests.Request(None, self.root + "/{}/".format(api_version) + endpoint,
                                   params=final_params, data=data, headers=headers)
        self.add_api_key(request)
        with requests.Session() as session:
            if request_type in ('get', 'post', 'put', 'delete'):
                request.method = request_type.upper()
            else:
                logger.critical('invalid request type {}'.format(request_type))

            if sign:
                self.sign_request_data(request, None, None)
            prepped = request.prepare()
            response = session.send(prepped)
        return response
