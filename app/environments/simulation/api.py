import base
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Environment(base.Environment):
    """
    An environment to simulate
    """
    # TODO: implement empty methods
    def __init__(self):
        super(Environment, self).__init__('Simulation', None)

    def parse_returned(self, returned):
        pass

    def hashify(self, url=None, data=None):
        pass

    def query_private(self, url, data=None, params=None, headers=None):
        pass

    def query_public(self, url, data=None, params=None, headers=None):
        pass

    def query(self, url, data=None, params=None, headers=None, post=False):
        pass

    def get_all_positions(self) -> list:
        pass

    def place_order(self):
        pass

    def get_current_rate(self, pair: str):
        pass

    def get_historical_prices(self, pair: str, interval: int):
        pass


if __name__ == '__main__':
    # test singleton
    env1 = Environment()
    env2 = Environment()
    print(env1 is env2)
