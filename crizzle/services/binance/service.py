import time
import hmac
import urllib
import logging
import hashlib
import requests
from crizzle.services.base import Service as BaseService

logger = logging.getLogger(__name__)


class Service(BaseService):
    # TODO: add postprocessing method deriving from base.service's postproc method
    def __init__(self, key_file=None):
        super(Service, self).__init__('Binance', "https://api.binance.com/api")
        self.default_api_version = 'v1'
        self.api_key, self.secret_key = self.load_key_file(key_file) if key_file is not None else (None, None)

    # region Helper methods
    @property
    def timestamp(self) -> int:
        return int(1000 * (time.time() - 1))

    def get_default_params(self, **kwargs):
        assert 'sign' in kwargs
        return {'timestamp': self.timestamp} if kwargs['sign'] else {}

    def load_key_file(self, key_file):
        if key_file is not None:
            with open(key_file, 'rb') as file:
                api_key = file.readline().strip()
                secret_key = file.readline().strip()
            return api_key, secret_key
        else:
            return None, None

    def validate_arguments(self, method, *args, **kwargs):
        if method == self.order:
            pass

    def add_api_key(self, request: requests.Request):
        """
        Adds API key to the request headers (in-place, does not create new copy of the request)

        Args:
            request (requests.Request): Request object to add the API key header to

        Returns:
            None
        """
        try:
            assert self.key_loaded
            request.headers['X-MBX-APIKEY'] = self.api_key
        except AssertionError:
            logger.error("API key has not been loaded. Unable to add API key to request headers.")

    def sign_request(self, request: requests.Request):
        encoded = bytes(urllib.parse.urlencode(request.params) + urllib.parse.urlencode(request.data), 'utf-8')
        signature = hmac.new(self.secret_key, encoded, digestmod=hashlib.sha256)
        request.params['signature'] = signature.hexdigest()
    # endregion

    # region Request Methods
    def get(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=False):
        return self.request('get', endpoint, params=params, api_version=api_version,
                            data=data, headers=headers, sign=sign)

    def post(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=True):
        return self.request('post', endpoint, params=params, api_version=api_version,
                            data=data, headers=headers, sign=sign)

    def put(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=True):
        return self.request('put', endpoint, params=params, api_version=api_version,
                            data=data, headers=headers, sign=sign)

    def delete(self, endpoint: str, params=None, api_version=None, data=None, headers=None, sign=True):
        return self.request('delete', endpoint, params=params, api_version=api_version,
                            data=data, headers=headers, sign=sign)
    # endregion

    # region General Endpoints
    def test_connection(self):
        return self.get("ping")

    def server_time(self):
        return self.get("time")

    def info(self, symbol=None, key=None):
        """
        Get information about a symbol or the exchange.
        if property is specified:
            if symbol is specified, returns specified property of that symbol.
            else, returns specified property of the exchange.

        Args:
            symbol: trading pair
            key: property of trading pair or exchange

        Returns:

        """
        info = self.get('exchangeInfo')
        if symbol is None:
            return info if key is None else info.json()[key]
        else:
            for pair in info.json()['symbols']:
                if pair['symbol'] == symbol:
                    return pair if key is None else pair[key]

    def trading_symbols(self):
        symbols = []
        symbol_info = self.info(key='symbols')
        for symbol in symbol_info:
            symbols.append(symbol['symbol'])
        return symbols

    # endregion

    # region Market Data Endpoints
    def depth(self, symbol: str):
        return self.get("depth", params={"symbol": symbol})

    def recent_trades(self, symbol: str, limit: int=None):
        params = {'symbol': symbol}
        if limit is None:
            params['limit'] = limit
        return self.get('trades', params=params)

    def historical_trades(self, symbol: str, limit: int=None, from_id: int=None):
        params = {'symbol': symbol}
        if limit is not None:
            params['limit'] = limit
        if from_id is not None:
            params['fromId'] = from_id
        return self.get('historicalTrades', params=params)

    def aggregated_trades(self, symbol: str, from_id: int = None, start: int = None, end: int = None,
                          limit: int = None):
        params = {'symbol': symbol}
        if from_id is not None:
            params['fromId'] = from_id
        if start is not None:
            params['startTime'] = start
        if end is not None:
            params['endTime'] = end
        if limit is not None:
            params['limit'] = limit
        return self.get('aggTrades', params=params)

    def candlesticks(self, symbol: str, interval: str, start=None, end=None):
        # TODO: enable conversion to Pandas Dataframe before returning
        params = {"symbol": symbol, "interval": interval}
        if start is not None and end is not None:
            params.update({"startTime": start, "endTime": end})
        return self.get("klines", params=params)

    def ticker_24(self, symbol: str):
        return self.get("ticker/24hr", params={"symbol": symbol})

    def ticker_price(self, symbol: str):
        return self.get("ticker/price", params={"symbol": symbol}, api_version='v3')

    def ticker_book(self, symbol: str):
        return self.get("ticker/bookTicker", params={"symbol": symbol}, api_version='v3')

    # endregion

    # region Account Endpoints
    def order(self, symbol, side, order_type, quantity, price: float=None, stop_price=None, time_in_force=None,
              iceberg_qty: float=None, client_order_id: str=None, test=False):
        # TODO: Implement global parameter checking
        params = {}
        params.update({'symbol': symbol, 'type': order_type, 'quantity': quantity, 'side': side})
        if price is not None:
            price = str(price)
        # region check order type
        if order_type == 'LIMIT':
            assert time_in_force is not None
            assert price is not None
            params.update({'timeInForce': time_in_force, 'price': price})
        elif order_type in ('STOP_LOSS', 'TAKE_PROFIT'):
            assert stop_price is not None
            params.update({'stopPrice': stop_price})
        elif order_type in ('STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT'):
            assert time_in_force is not None
            assert stop_price is not None
            assert price is not None
            params.update({'stopPrice': stop_price, 'price': price, 'timeInForce': time_in_force})
        elif order_type == 'LIMIT_MAKER':
            assert price is not None
            params.update({'price': price})
        else:
            raise ValueError('Invalid order type')
        # endregion
        # region check iceberg paramters
        if iceberg_qty is not None:
            assert time_in_force == 'GTC'
            params['icebergQty'] = iceberg_qty
        # endregion
        if client_order_id is not None:
            params['newClientOrderId'] = client_order_id
        assert side in ('BUY', 'SELL')
        assert time_in_force in (None, 'GTC', 'IOC', 'FOK')
        return self.post('order{}'.format('/test' if test else ''), api_version='v3', params=params, sign=True)

    def test_order(self, symbol, side, order_type, quantity, price=None, stop_price=None, time_in_force=None,
                   iceberg_qty=None, client_order_id=None):
        return self.order(symbol, side, order_type, quantity, price=price, stop_price=stop_price,
                          time_in_force=time_in_force, iceberg_qty=iceberg_qty,
                          client_order_id=client_order_id, test=True)

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
        return self.delete('order', api_version='v3', params=params)

    def query_order(self, symbol: str, order_id=None, original_client_order_id=None):
        params = {'symbol': symbol}
        if order_id is None and original_client_order_id is None:
            raise ValueError('Either orderId or origClientOrderId must be provided for cancellation.')
        elif order_id is not None:
            params['orderId'] = order_id
        elif original_client_order_id is not None:
            params['origClientOrderId'] = original_client_order_id
        return self.get('order', api_version='v3', params=params, sign=True)

    def open_orders(self, symbol=None):
        params = {}
        if symbol is not None:
            params['symbol'] = symbol
        return self.get('openOrders', api_version='v3', params=params, sign=True)

    def all_orders(self, symbol, order_id=None, limit=None):
        params = {'symbol': symbol}
        if order_id is not None:
            params['order_id'] = order_id
        if limit is not None:
            params['limit'] = limit
        return self.get('allOrders', api_version='v3', params=params, sign=True)

    def account_info(self):
        return self.get('account', api_version='v3', params=None, sign=True)

    def trade_list(self, symbol, limit: int=None, from_id: int=None):
        params = {'symbol': symbol}
        if limit is not None:
            params['limit'] = limit
        if from_id is not None:
            params['fromId'] = from_id
        return self.get('myTrades', api_version='v3', params=params, sign=True)

    # endregion

    pass


if __name__ == '__main__':
    grabber = Service(key_file="G:\\Documents\\Python Scripts\\crizzle\\data\\keys\\binance.apikey")
    test_env = Service(key_file="G:\\Documents\\Python Scripts\\crizzle\\data\\keys\\binance_test.apikey")

    # def test_authenticate_request():
    #     request = requests.Request('GET', "https://api.binance.com/api/v3/order",
    #                                params={'symbol': 'LTCBTC', 'side': 'BUY', 'type': 'LIMIT', 'timeInForce': 'GTC'},
    #                                data={'quantity': 1, 'price': '0.1', 'recvWindow': 5000, 'timestamp': 1499827319559})
    #     print(urllib.parse.urlencode(request.params) + urllib.parse.urlencode(request.data))
    #     test_env.sign_request(request)
    #     print(request.params)
    #     if request.params['signature'] != '0fd168b8ddb4876a0358a8d14d0c9f3da0e9b20c5d52b2a00fcf7d1c602f9a77':
    #         print('failed')
    #     else:
    #         print('passed')

    # test_authenticate_request()


    # print(grabber.test_connection())
    # print(grabber.historical_trades('TRXETH').json())
    # print(grabber.info('BATETH', 'filters'))
    # order = grabber.order('ETHBTC', 'BUY', 'LIMIT', 0.013, price=0.08, time_in_force='GTC')
    # print(order.json())
    # cancel = grabber.cancel_order('ETHBTC', order_id=77546685)
    # print(cancel.json())
    # print(grabber.recent_trades('ETHBTC'))

    # print(grabber.candlesticks("ETHBTC", '1h'))
    # print(grabber.candlesticks("EOSETH", "1h"))
