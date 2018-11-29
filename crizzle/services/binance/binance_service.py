import os
import time
import hmac
import random
import json
import urllib
import logging
import hashlib
from ratelimit import RateLimitException, limits, sleep_and_retry
from backoff import on_exception, expo
from crizzle.services.base import Service
from crizzle.services.binance.rate_limiter import RateLimiter
from crizzle import utils

logger = logging.getLogger(__name__)


class Constants:
    TIME_MULTIPLIER = 1000
    INTERVAL_1MINUTE = '1m'
    INTERVAL_3MINUTE = '3m'
    INTERVAL_5MINUTE = '5m'
    INTERVAL_15MINUTE = '15m'
    INTERVAL_30MINUTE = '30m'
    INTERVAL_1HOUR = '1h'
    INTERVAL_2HOUR = '2h'
    INTERVAL_4HOUR = '4h'
    INTERVAL_6HOUR = '6h'
    INTERVAL_8HOUR = '8h'
    INTERVAL_12HOUR = '12h'
    INTERVAL_1DAY = '1d'
    INTERVAL_1WEEK = '1w'
    INTERVAL_1MONTH = '1M'
    INTERVALS = [INTERVAL_1MINUTE, INTERVAL_3MINUTE, INTERVAL_5MINUTE, INTERVAL_15MINUTE,
                 INTERVAL_30MINUTE, INTERVAL_1HOUR, INTERVAL_2HOUR, INTERVAL_4HOUR,
                 INTERVAL_6HOUR, INTERVAL_8HOUR, INTERVAL_12HOUR, INTERVAL_1DAY,
                 INTERVAL_1WEEK, INTERVAL_1MONTH
                 ]
    INTERVAL_SUFFIX_MAP = {'m': 60, 'h': 3600, 'd': 24 * 3600, 'w': 7 * 24 * 3600, 'M': 30 * 24 * 3600}

    @staticmethod
    def interval_value(interval):
        suffix = interval[-1]
        interval = int(interval[:-1])
        return interval * Constants.INTERVAL_SUFFIX_MAP[suffix] * Constants.TIME_MULTIPLIER


class BinanceService(Service):
    constants = Constants

    def __init__(self, key=None, debug=False, recv_window=5000, name=None, default_timestamp=None):
        super(BinanceService, self).__init__('binance' if name is None else name,
                                             "https://api.binance.com/api",
                                             debug=debug,
                                             default_timestamp=default_timestamp,
                                             key=key)
        self.rate_limited = False
        self.default_api_version = 'v1'
        self.recv_window = recv_window

    # region Helper methods
    @property
    def key(self):
        key = self._get_key()
        if key is None:
            return {'key': None, 'secret': None}
        else:
            assert 'key' in key
            assert 'secret' in key
            return {'key': key['key'], 'secret': key['secret']}

    @property
    def api_key(self):
        return self.key['key']

    @property
    def secret_key(self):
        return self.key['secret']

    @property
    def key_loaded(self):
        return self.api_key is not None and self.secret_key is not None

    @property
    def timestamp(self) -> int:
        if self.debug:
            return self.default_timestamp
        else:
            return super(BinanceService, self).timestamp

    def get_default_params(self, **kwargs):
        assert 'sign' in kwargs
        return {'timestamp': self.timestamp, 'recvWindow': self.recv_window} if kwargs['sign'] else {}

    def add_api_key(self, params=None, data=None, headers=None):
        """
        Adds API key to the request params/data/headers.

        Args:
            params (dict): request params
            data (dict): request data
            headers (dict): request headers

        Returns:
            None
        """
        if not self.key_loaded:
            raise RuntimeError("API key has not been loaded. Unable to add API key to request headers.")
        else:
            headers['X-MBX-APIKEY'] = self.api_key
        return {'params': params, 'data': data, 'headers': headers}

    def sign_request_data(self, params=None, data=None, headers=None):
        """
        Sign the request params/data/headers with the secret key.

        Args:
            params (dict): request params
            data (dict): request data
            headers (dict): request headers

        Returns:

        """
        if not self.key_loaded:
            raise RuntimeError("API key has not been loaded. Unable to sign request.")
        encoded = bytes(urllib.parse.urlencode(params) + urllib.parse.urlencode(data), 'utf-8')
        signature = hmac.new(bytes(self.secret_key, 'utf-8'), encoded, digestmod=hashlib.sha256)
        params['signature'] = signature.hexdigest()
        return {'params': params, 'data': data, 'headers': headers}
    # endregion

    @sleep_and_retry
    @limits(calls=75, period=5)
    def request(self, request_type: str, endpoint: str, params=None, api_version=None, data=None, headers=None,
                sign=False, add_api_key=True):
        if self.rate_limited:
            raise RateLimitException('Binance rate limit reached.', 60)
        response = super(BinanceService, self).request(request_type, endpoint, params=params, api_version=api_version,
                                                       data=data, headers=headers, sign=sign, add_api_key=add_api_key)
        if not self.debug:
            if response.status_code in {429, 418}:
                self.rate_limited = True
                logger.critical("Binance rate limit reached.")
                raise RateLimitException('Binance rate limit reached.', 60)
            if response.status_code == 403:
                self.rate_limited = True
                logger.critical("Binance API has blocked this client.")
                raise RateLimitException('Binance has blocked this client. Pausing all activity for 5 minutes.', 300)
        self.rate_limited = False
        return response

    # region General Endpoints
    def test_connection(self):
        return self.get('ping', add_api_key=False)

    def server_time(self):
        return self.get("time", add_api_key=False)

    def info(self):
        """
        Get information about the exchange.
        """
        return self.get("exchangeInfo", add_api_key=False)

    def trading_assets(self):
        """
        Get the set of all trading

        Returns:

        """
        info = self.info()
        if self.debug:
            return info
        else:
            symbols = info.json()['symbols']
            assets = set()
            for symbol in symbols:
                if symbol['status'] == 'TRADING':
                    base = symbol['baseAsset']
                    quote = symbol['quoteAsset']
                    assets.add(base)
                    assets.add(quote)
            return assets

    def trading_symbols(self):
        """
        Get a list of all symbols trading on the exchange.

        Returns:
            list: Symbols trading on the exchange.
        """
        symbols = []
        info = self.info()
        if self.debug:
            return info
        else:
            symbol_info = info.json()['symbols']
            for symbol in symbol_info:
                if symbol['status'] == 'TRADING':
                    symbols.append(symbol['symbol'])
            return symbols

    # endregion

    # region Market Data Endpoints
    def depth(self, symbol: str, limit=None):
        """
        Get depth information.

        Args:
            symbol: Which trading symbol to get depth info for
            limit: Number of price points to aggregate orders into

        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        response = self.get("depth", params=params)
        return response

    def recent_trades(self, symbol: str, limit: int = None):
        params = {'symbol': symbol}
        if limit is not None:
            params['limit'] = limit
        response = self.get('trades', params=params)
        return response

    def historical_trades(self, symbol: str, limit: int = None, from_id: int = None):
        params = {'symbol': symbol}
        if limit is not None:
            params['limit'] = limit
        if from_id is not None:
            params['fromId'] = from_id
        response = self.get('historicalTrades', params=params)
        return response

    def aggregated_trades(self, symbol: str, from_id: int = None, start: int = None, end: int = None,
                          limit: int = None):
        if start is not None and len(str(abs(start))) < 13:
            start = self.time_multiplier * start
        if end is not None and len(str(abs(end))) < 13:
            end = self.time_multiplier * end
        params = {'symbol': symbol}
        if from_id is not None:
            params['fromId'] = from_id
        if start is not None:
            params['startTime'] = start
        if end is not None:
            params['endTime'] = end
        if limit is not None:
            params['limit'] = limit
        response = self.get('aggTrades', params=params)
        return response

    def candlesticks(self, symbol: str, interval: str, limit=None, start=None, end=None):
        if start is not None and len(str(abs(start))) < 13:
            start = self.time_multiplier * start
        if end is not None and len(str(abs(end))) < 13:
            end = self.time_multiplier * end
        params = {"symbol": symbol, "interval": interval}
        if start is not None:
            params.update({"startTime": start})
        if end is not None:
            params.update({"endTime": end})
        if limit is not None:
            params['limit'] = limit
        response = self.get("klines", params=params)
        return response

    def ticker_24(self, symbol: str = None):
        params = {}
        if symbol is not None:
            params['symbol'] = symbol
        response = self.get("ticker/24hr", params=params)
        return response

    def ticker_price(self, symbol=None):
        response = self.get("ticker/price", params=None, api_version='v3')
        if not self.debug:
            response = {item['symbol']: float(item['price']) for item in response.json()}
            if isinstance(symbol, str):
                response = [v for k, v in response.items() if k == symbol][0]
            elif isinstance(symbol, (list, tuple)):
                response = {k: v for k, v in response.items() if k in symbol}
            if not response:
                raise ValueError("Invalid symbol(s) of type {}: {}".format(type(symbol), symbol))
        return response

    def ticker_book(self, symbol: str = None):
        params = {}
        if symbol is not None:
            params['symbol'] = symbol
        response = self.get("ticker/bookTicker", params=params, api_version='v3')
        return response

    # endregion

    # region Account Endpoints
    def order(self, symbol, side, order_type, quantity, price: float = None, stop_price=None, time_in_force: str = None,
              iceberg_qty: float = None, new_client_order_id: int = None, test=False):
        params = {'newOrderRespType': 'FULL'}
        side = side.upper()
        order_type = order_type.upper()
        if time_in_force is not None:
            time_in_force = time_in_force.upper()
        if price is not None:
            price = utils.misc.float_to_str(price)

        if order_type == 'LIMIT':
            utils.assert_none(stop_price, 'stop_price')
            utils.assert_not_none(time_in_force, 'time_in_force')
            utils.assert_not_none(price, 'price')
            params.update({'timeInForce': time_in_force, 'price': price})
        elif order_type == 'MARKET':
            utils.assert_none(price, 'price')
            utils.assert_not_none(quantity, 'quantity')
        elif order_type in ('STOP_LOSS', 'TAKE_PROFIT'):
            utils.assert_not_none(stop_price, 'stop_price')
            params.update({'stopPrice': stop_price})
        elif order_type in ('STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT'):
            utils.assert_not_none(time_in_force, 'time_in_force')
            utils.assert_not_none(stop_price, 'stop_price')
            utils.assert_not_none(price, 'price')
            params.update({'stopPrice': stop_price, 'price': price, 'timeInForce': time_in_force})
        elif order_type == 'LIMIT_MAKER':
            utils.assert_not_none(price, 'price')
            params.update({'price': price})
        else:
            raise ValueError('Invalid order type')
        if iceberg_qty is not None:
            utils.assert_equal(time_in_force, 'time_in_force', 'GTC')
            params['icebergQty'] = iceberg_qty
        if new_client_order_id is not None:
            params['newClientOrderId'] = new_client_order_id
        utils.assert_in(side, 'side', ('BUY', 'SELL'))
        utils.assert_in(time_in_force, 'time_in_force', (None, 'GTC', 'IOC', 'FOK'))
        params.update({'symbol': symbol, 'type': order_type, 'quantity': quantity, 'side': side})
        response = self.post('order{}'.format('/test' if test else ''), api_version='v3', params=params, sign=True)
        return response

    def test_order(self, symbol, side, order_type, quantity, price=None, stop_price=None, time_in_force=None,
                   iceberg_qty=None, client_order_id=None):
        response = self.order(symbol, side, order_type, quantity, price=price, stop_price=stop_price,
                              time_in_force=time_in_force, iceberg_qty=iceberg_qty,
                              new_client_order_id=client_order_id, test=True)
        return response

    def cancel_order(self, symbol: str, order_id=None, original_client_order_id=None, new_client_order_id=None):
        params = {'symbol': symbol}
        if order_id is None and original_client_order_id is None:
            raise ValueError('Either orderId or origClientOrderId must be provided for cancellation.')
        elif order_id is not None:
            params['orderId'] = order_id
        elif original_client_order_id is not None:
            params['origClientOrderId'] = original_client_order_id
        if new_client_order_id is not None:
            params['newClientOrderId'] = new_client_order_id
        response = self.delete('order', api_version='v3', params=params)
        return response

    def query_order(self, symbol: str, order_id=None, original_client_order_id=None):
        params = {'symbol': symbol}
        if order_id is None and original_client_order_id is None:
            raise ValueError('Either orderId or origClientOrderId must be provided for cancellation.')
        elif order_id is not None:
            params['orderId'] = order_id
        elif original_client_order_id is not None:
            params['origClientOrderId'] = original_client_order_id
        response = self.get('order', api_version='v3', params=params, sign=True)
        return response

    def open_orders(self, symbol=None):
        params = {}
        if symbol is not None:
            params['symbol'] = symbol
        response = self.get('openOrders', api_version='v3', params=params, sign=True)
        return response

    def all_orders(self, symbol, order_id=None, limit=None):
        params = {'symbol': symbol}
        if order_id is not None:
            params['orderId'] = order_id
        if limit is not None:
            params['limit'] = limit
        response = self.get('allOrders', api_version='v3', params=params, sign=True)
        return response

    def account_info(self):
        response = self.get('account', api_version='v3', params=None, sign=True)
        return response

    def my_trades(self, symbol, limit: int = None, from_id: int = None):
        params = {'symbol': symbol}
        if limit is not None:
            params['limit'] = limit
        if from_id is not None:
            params['fromId'] = from_id
        response = self.get('myTrades', api_version='v3', params=params, sign=True)
        return response

    # endregion
