import time
import logging
import hmac
import urllib
import hashlib
import requests
from crizzle.data.data_grabber import DataGrabber

logger = logging.getLogger(__name__)


class BinanceDataGrabber(DataGrabber):
    def __init__(self, key_file=None):
        super(BinanceDataGrabber, self).__init__()
        self.default_api_version = 1
        self.root = "https://api.binance.com/api/"
        self._api_key, self._secret_key = self.__load_key_file(key_file)

    def __load_key_file(self, key_file):
        if key_file is not None:
            with open(key_file, 'rb') as file:
                api_key = file.readline().strip()
                secret_key = file.readline().strip()
            return (api_key, secret_key)
        else:
            return (None, None)

    def public_request(self, endpoint: str, params=None, api_version=None):
        if api_version is None:
            api_version = self.default_api_version
        return requests.get(self.root + "v{}/".format(api_version) + endpoint, params=params)

    def private_request(self, endpoint: str, params=None, api_version=None, payload=None, headers=None):
        if api_version is None:
            api_version = self.default_api_version

        request = requests.Request('GET',
                                   self.root + "v{}/".format(api_version) + endpoint,
                                   params=params,
                                   headers=headers)
        request.headers['X-MBX-APIKEY'] = self._api_key
        b = bytes(urllib.parse.urlencode(request.params), 'utf-8')
        signature = hmac.new(self._secret_key, b, digestmod=hashlib.sha256)
        request.params['signature'] = signature.hexdigest()
        prepped = request.prepare()

        with requests.Session() as sess:
            response = sess.send(prepped)
        return response

    def test_connection(self):
        return self.public_request("ping").json()

    def server_time(self):
        return self.public_request("time").json()

    def depth(self, symbol: str):
        return self.public_request("depth", {"symbol": symbol}).json()

    def ticker_24(self, symbol: str):
        return self.public_request("ticker/24hr", params={"symbol": symbol}).json()

    def ticker_price(self, symbol: str):
        return self.public_request("ticker/price", params={"symbol": symbol}, api_version=3).json()

    def candlesticks(self, symbol: str, interval: str, start: int=None, end: int=None):
        params = {"symbol": symbol, "interval": interval}
        if start is not None and end is not None:
            params.update({"startTime": start, "endTime": end})
        return self.public_request("klines", params=params).json()

    @staticmethod
    def clean_response(response):
        return response.json()

    def next(self):
        pass
    def _subscribe(self):
        pass


if __name__ == '__main__':
    import pprint

    pp = pprint.PrettyPrinter(indent=2)
    grabber = BinanceDataGrabber(key_file="G:\\Documents\\Python Scripts\\Crypto_Algotrader\\binance.key")

    print(grabber.private_request('account', api_version=3, params={'timestamp': int(1000 * time.time())}).content)


    # print(grabber.candlesticks("EOSETH", "1h"))
    # print(grabber.candlesticks("EOSETH", "1h"))

