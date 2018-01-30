import time
import logging
from abc import ABCMeta, abstractmethod
from crizzle.data.exchange_data_grabber import ExchangeDataGrabber
import requests

logger = logging.getLogger(__name__)


class BinanceDataGrabber(ExchangeDataGrabber):
    def __init__(self):
        super(BinanceDataGrabber, self).__init__(root="https://api.binance.com/api/v1/")

    def test_connection(self):
        return requests.get(self.source + "ping").json()

    def server_time(self):
        return requests.get(self.source + "time").json()

    def next(self):
        pass

    def _subscribe(self):
        pass



if __name__ == '__main__':
    grabber = BinanceDataGrabber()

    t = time.time()
    print(grabber.test_connection())
    print(time.time() - t)

    t = time.time()
    print(grabber.server_time())
    print(time.time() - t)
