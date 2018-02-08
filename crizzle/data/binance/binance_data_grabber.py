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
        self._api_key, self._secret_key = self._load_key_file(key_file)

    @staticmethod
    def _load_key_file(key_file):
        if key_file is not None:
            with open(key_file, 'rb') as file:
                api_key = file.readline().strip()
                secret_key = file.readline().strip()
            return api_key, secret_key
        else:
            return None, None

    @staticmethod
    def _timestamp()->int:
        return int(1000 * time.time())

    @property
    def default_params(self):
        return {'timestamp': self._timestamp()}

    def public_request(self, endpoint: str, params=None, api_version=None):
        if api_version is None:
            api_version = self.default_api_version
        return requests.get(self.root + "v{}/".format(api_version) + endpoint, params=params)

    def private_request(self, endpoint: str, params=None, api_version=None, data=None, headers=None, post=False):
        if api_version is None:
            api_version = self.default_api_version

        request = requests.Request('POST' if post else 'GET',
                                   self.root + "v{}/".format(api_version) + endpoint,
                                   params=params,
                                   data=data,
                                   headers=headers)
        request.headers['X-MBX-APIKEY'] = self._api_key
        b = bytes(urllib.parse.urlencode(request.data if post else request.params), 'utf-8')
        signature = hmac.new(self._secret_key, b, digestmod=hashlib.sha256)
        if post:
            request.data['signature'] = signature.hexdigest()
        else:
            request.params['signature'] = signature.hexdigest()
        prepped = request.prepare()

        with requests.Session() as sess:
            response = sess.send(prepped)
        return response

    # region General Endpoints
    def test_connection(self):
        return self.public_request("ping").json()

    def server_time(self):
        return self.public_request("time").json()

    def info(self, symbol=None, property=None):
        """
        Get information about a symbol or the exchange.
        if property is specified:
            if symbol is specified, returns specified property of that symbol.
            else, returns specified property of the exchange.

        Args:
            symbol: trading pair
            property: property of trading pair or exchange

        Returns:

        """
        info = self.public_request('exchangeInfo').json()
        if symbol is None:
            return info if property is None else info[property]
        else:
            for pair in info['symbols']:
                if pair['symbol'] == symbol:
                    return pair if property is None else pair[property]
    # endregion

    # region Market Data Endpoints
    def depth(self, symbol: str):
        return self.public_request("depth", {"symbol": symbol}).json()

    def trade_list(self, symbol: str, limit: int=None):
        if limit is None:
            return self.public_request('trades')
        else:
            return self.public_request('trades', params={'limit': int})

    def historical_trades(self, symbol: str, limit: int=None, from_id: int=None):
        params = {'symbol': symbol}
        if limit is not None:
            params['limit'] = limit
        if from_id is not None:
            params['fromId'] = from_id
        return self.public_request('historicalTrades', params=params)

    def aggregated_trades(self, symbol: str, from_id: int=None, start: int=None, end: int=None, limit: int=None):
        params = {'symbol': symbol}
        if from_id is not None:
            params['fromId'] = from_id
        if start is not None:
            params['startTime'] = start
        if end is not None:
            params['endTime'] = end
        if limit is not None:
            params['limit'] = limit
        return self.public_request('aggTrades', params=params)

    def candlesticks(self, symbol: str, interval: str, start: int=None, end: int=None):
        params = {"symbol": symbol, "interval": interval}
        if start is not None and end is not None:
            params.update({"startTime": start, "endTime": end})
        return self.public_request("klines", params=params).json()

    def ticker_24(self, symbol: str):
        return self.public_request("ticker/24hr", params={"symbol": symbol}).json()

    def ticker_price(self, symbol: str):
        return self.public_request("ticker/price", params={"symbol": symbol}, api_version=3).json()

    def ticker_book(self, symbol: str):
        return self.public_request("ticker/bookTicker", params={"symbol": symbol}, api_version=3).json()

    # endregion

    # region Account Endpoints
    def account_info(self):
        return self.private_request('account', api_version=3, params=self.default_params).json()

    def order(self, symbol, side, type, quantity, price=None, stop_price=None, time_in_force=None, iceberg_qty=None, client_order_id=None, test=False):
        data = self.default_params
        data.update({'symbol': symbol, 'type': type, 'quantity': quantity, 'side': side})

        try:
            if type == 'LIMIT':
                assert time_in_force is not None
                assert price is not None
                data.update({'timeInForce': time_in_force, 'price': price})
            elif type in ('STOP_LOSS', 'TAKE_PROFIT'):
                assert stop_price is not None
                data.update({'stopPrice': stop_price})
            elif type in ('STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT'):
                assert time_in_force is not None
                assert stop_price is not None
                assert price is not None
                data.update({'stopPrice': stop_price, 'price': price, 'timeInForce': time_in_force})
            elif type == 'LIMIT_MAKER':
                assert price is not None
                data.update({'price': price})
            else:
                raise ValueError('Invalid order type')
        except ValueError as e:
            pass
        except AssertionError as e:
            pass

        try:
            assert side in ('BUY', 'SELL')
            assert time_in_force in (None, 'GTC', 'IOC', 'FOK')
        except AssertionError as e:
            pass

        return self.private_request('order{}'.format('/test' if test else ''), api_version=3, data=data, post=True).json()

    def test_order(self, symbol, side, type, quantity, price=None, stop_price=None, time_in_force=None, iceberg_qty=None, client_order_id=None):
        return self.order(symbol, side, type, quantity, price=price, stop_price=stop_price, time_in_force=time_in_force, iceberg_qty=iceberg_qty, client_order_id=client_order_id, test=True)

    def cancel_order(self, ):
        pass

    # endregion

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
    grabber = BinanceDataGrabber(key_file="G:\\Documents\\Python Scripts\\crizzle\\binance.key")

    # print(grabber.account_info())
    # print(grabber.info('BATETH', 'filters'))
    print(grabber.test_order('EOSETH', 'BUY', 'LIMIT', 1, price=0.01076, time_in_force='GTC'))

    # print(grabber.candlesticks("EOSETH", "1h"))
    # print(grabber.candlesticks("EOSETH", "1h"))

