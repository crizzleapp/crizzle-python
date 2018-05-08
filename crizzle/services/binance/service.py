import time
import hmac
import json
import urllib
import logging
import hashlib
import pandas as pd
from crizzle.services.base import Service as BaseService
from crizzle import patterns

logger = logging.getLogger(__name__)


class Service(BaseService):
    def __init__(self, key=None, debug=False, mode='json', recv_window=None):
        super(Service, self).__init__('binance', "https://api.binance.com/api", debug=debug)
        self.mode = mode
        self.timestamp_unit = 'ms'
        self.default_api_version = 'v1'
        self.recv_window = 5000 if recv_window is None else recv_window

    # region Helper methods
    @property
    def timestamp(self) -> int:
        return int(1000 * (time.time() - 1))

    def get_default_params(self, **kwargs):
        assert 'sign' in kwargs
        return {'timestamp': self.timestamp, 'recvWindow': self.recv_window} if kwargs['sign'] else {}

    def add_api_key(self, params=None, data=None, headers=None):
        """
        Adds API key to the request headers (in-place, does not create new copy of the request)

        Args:
            request (requests.Request): Request object to add the API key header to

        Returns:
            None
        """
        try:
            assert self.key_loaded
            headers['X-MBX-APIKEY'] = self.api_key
        except AssertionError:
            logger.error("API key has not been loaded. Unable to add API key to request headers.")

    def sign_request_data(self, params=None, data=None, headers=None):
        encoded = bytes(urllib.parse.urlencode(params) + urllib.parse.urlencode(data), 'utf-8')
        signature = hmac.new(self.secret_key, encoded, digestmod=hashlib.sha256)
        params['signature'] = signature.hexdigest()

    # endregion

    # region General Endpoints
    def test_connection(self):
        return self.get('ping')

    def server_time(self):
        response = self.get("time")
        if self.debug:
            return response
        else:
            return response.json()['serverTime']

    def info(self, symbol=None, key=None):
        """
        Get information about a symbol or the exchange.
        if key is specified:
            if symbol is specified, returns specified property of that symbol.
            else, returns specified property of the exchange.

        Args:
            symbol: trading pair
            key: property of trading pair or exchange

        Returns:

        """
        response = self.get('exchangeInfo')
        if self.debug:
            return response.json()
        else:
            if symbol is None:
                return response if key is None else response.json()[key]
            else:
                for pair in response.json()['symbols']:
                    if pair['symbol'] == symbol:
                        return pair if key is None else pair[key]

    def trading_assets(self):
        """


        Returns:

        """
        symbols = self.info(key='symbols')
        assets = set()
        for symbol in symbols:
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
        symbol_info = self.info(key='symbols')
        for symbol in symbol_info:
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

        Returns:
            dict: 'asks' - Dataframe of asks depth
            'bids': Dataframe of bids depth
            'last': Last update ID
        """
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        response = self.get("depth", params=params)
        if self.debug:
            return response
        elif self.mode == 'pandas':
            data = response.json()
            asks = pd.DataFrame(data['asks'], columns=['price', 'quantity', 'ignore'], dtype=float)
            asks.pop('ignore')
            bids = pd.DataFrame(data['bids'], columns=['price', 'quantity', 'ignore'], dtype=float)
            bids.pop('ignore')
            return {'asks': asks, 'bids': bids, 'last': data['lastUpdateId']}
        elif self.mode == 'json':
            return response.json()

    def recent_trades(self, symbol: str, limit: int = None):
        params = {'symbol': symbol}
        if limit is not None:
            params['limit'] = limit
        response = self.get('trades', params=params)
        if self.debug:
            return response
        elif self.mode == 'pandas':
            df = pd.DataFrame(response.json())
            df['timestamp'] = df['time']
            df['time'] = pd.to_datetime(df['time'], unit=self.timestamp_unit)
            df[['price', 'quantity']] = df[['price', 'quantity']].astype(float)
            return df
        elif self.mode == 'json':
            return response.json()

    def historical_trades(self, symbol: str, limit: int = None, from_id: int = None):
        params = {'symbol': symbol}
        if limit is not None:
            params['limit'] = limit
        if from_id is not None:
            params['fromId'] = from_id
        response = self.get('historicalTrades', params=params)
        if self.debug:
            return response
        elif self.mode == 'pandas':
            df = pd.DataFrame(response.json())
            df['timestamp'] = df['time']
            df['time'] = pd.to_datetime(df['time'], unit=self.timestamp_unit)
            df[['price', 'quantity']] = df[['price', 'quantity']].astype(float)
            return df
        elif self.mode == 'json':
            return response.json()

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
        response = self.get('aggTrades', params=params)
        if self.debug:
            return response
        elif self.mode == 'pandas':
            df = pd.DataFrame(response.json())
            df['id'] = df.pop('a')
            df['price'] = df.pop('p').astype(float)
            df['quantity'] = df.pop('q').astype(float)
            df['firstId'] = df.pop('f')
            df['lastId'] = df.pop('l')
            df['timestamp'] = df.pop('T')
            df['time'] = pd.to_datetime(df['timestamp'], unit=self.timestamp_unit)
            df['isBuyerMaker'] = df.pop('m')
            df['isBestMatch'] = df.pop('M')
            return df
        elif self.mode == 'json':
            return response.json()

    def candlesticks(self, symbol: str, interval: str, limit=None, start=None, end=None):
        params = {"symbol": symbol, "interval": interval}
        if start is not None:
            params.update({"startTime": start})
        if end is not None:
            params.update({"endTime": end})
        if limit is not None:
            params['limit'] = limit
        response = self.get("klines", params=params)
        if self.debug:
            return response
        else:
            df = pd.DataFrame(response.json(), columns=['openTimestamp', 'open', 'high', 'low', 'close', 'volume',
                                                        'closeTimestamp', 'quoteVolume', 'numTrades',
                                                        'takerBuyBaseVolume',
                                                        'takerBuyQuoteVolume', 'ignore'])
            df.pop('ignore')
            df = df.apply(pd.to_numeric)
            df['openTime'] = pd.to_datetime(df['openTimestamp'], unit=self.timestamp_unit)
            df['closeTime'] = pd.to_datetime(df['closeTimestamp'], unit=self.timestamp_unit)
            if self.mode == 'pandas':
                return df
            elif self.mode == 'json':
                return json.loads(df.to_json(orient='records', date_format='iso'))

    def ticker_24(self, symbol: str = None):
        params = {}
        if symbol is not None:
            params['symbol'] = symbol
        response = self.get("ticker/24hr", params=params)
        if self.debug:
            return response
        elif self.mode == 'pandas':
            if symbol is not None:
                df = pd.DataFrame(response.json(), index=[0])
            else:
                df = pd.DataFrame(response.json())
            return df
        elif self.mode == 'json':
            return response.json()

    def ticker_price(self, symbol: str = None):
        params = {}
        if symbol is not None:
            params['symbol'] = symbol
        response = self.get("ticker/price", params=params, api_version='v3')
        if self.debug:
            return response
        elif self.mode == 'pandas':
            if symbol is None:
                df = pd.DataFrame(response.json())
            else:
                df = pd.DataFrame(response.json(), index=[0])
            df.price = df.price.astype('float')
            return df
        elif self.mode == 'json':
            return response.json()

    def ticker_book(self, symbol: str = None):
        params = {}
        if symbol is not None:
            params['symbol'] = symbol
        response = self.get("ticker/bookTicker", params=params, api_version='v3')
        if self.debug:
            return response
        elif self.mode == 'pandas':
            if symbol is not None:
                df = pd.DataFrame(response.json(), index=[0])
            else:
                df = pd.DataFrame(response.json())
            return df
        elif self.mode == 'json':
            return response.json()

    # endregion

    # region Account Endpoints
    def order(self, symbol, side, order_type, quantity, price: float = None, stop_price=None, time_in_force: str = None,
              iceberg_qty: float = None, client_order_id: str = None, test=False):
        params = {}
        side = side.upper()
        order_type = order_type.upper()
        if time_in_force is not None:
            time_in_force = time_in_force.upper()
        if price is not None:
            price = patterns.conversion.float_to_str(price)
            print(price)
        if order_type == 'LIMIT':
            try:
                patterns.assert_none(stop_price, 'stop_price')
                patterns.assert_not_none(time_in_force, 'time_in_force')
                patterns.assert_not_none(price, 'price')
            except ValueError as e:
                logger.exception(str(e))
                raise e
            params.update({'timeInForce': time_in_force, 'price': price})
        elif order_type == 'MARKET':
            try:
                patterns.assert_none(price, 'price')
                patterns.assert_not_none(quantity, 'quantity')
            except ValueError as e:
                logger.exception(str(e))
                raise
        elif order_type in ('STOP_LOSS', 'TAKE_PROFIT'):
            try:
                patterns.assert_not_none(stop_price, 'stop_price')
            except ValueError as e:
                logger.exception(str(e))
                raise e
            params.update({'stopPrice': stop_price})
        elif order_type in ('STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT'):
            try:
                patterns.assert_not_none(time_in_force, 'time_in_force')
                patterns.assert_not_none(stop_price, 'stop_price')
                patterns.assert_not_none(price, 'price')
            except ValueError as e:
                logger.exception(str(e))
                raise e
            params.update({'stopPrice': stop_price, 'price': price, 'timeInForce': time_in_force})
        elif order_type == 'LIMIT_MAKER':
            try:
                patterns.assert_not_none(price, 'price')
            except ValueError as e:
                logger.exception(str(e))
                raise e
            params.update({'price': price})
        else:
            raise ValueError('Invalid order type')
        try:
            if iceberg_qty is not None:
                patterns.assert_equal(time_in_force, 'time_in_force', 'GTC')
                params['icebergQty'] = iceberg_qty
        except ValueError as e:
            logger.exception(str(e))
            raise e
        if client_order_id is not None:
            params['newClientOrderId'] = client_order_id
        try:
            patterns.assert_in(side, 'side', ('BUY', 'SELL'))
            patterns.assert_in(time_in_force, 'time_in_force', (None, 'GTC', 'IOC', 'FOK'))
        except ValueError as e:
            logger.exception(str(e))
            raise e
        params.update({'symbol': symbol, 'type': order_type, 'quantity': quantity, 'side': side})
        response = self.post('order{}'.format('/test' if test else ''), api_version='v3', params=params, sign=True)
        if self.debug:
            return response
        else:
            return response.json()

    def test_order(self, symbol, side, order_type, quantity, price=None, stop_price=None, time_in_force=None,
                   iceberg_qty=None, client_order_id=None):
        response = self.order(symbol, side, order_type, quantity, price=price, stop_price=stop_price,
                              time_in_force=time_in_force, iceberg_qty=iceberg_qty,
                              client_order_id=client_order_id, test=True)
        if self.debug:
            return response
        else:
            return response.content

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
        if self.debug:
            return response
        else:
            return response.json()

    def query_order(self, symbol: str, order_id=None, original_client_order_id=None):
        params = {'symbol': symbol}
        if order_id is None and original_client_order_id is None:
            raise ValueError('Either orderId or origClientOrderId must be provided for cancellation.')
        elif order_id is not None:
            params['orderId'] = order_id
        elif original_client_order_id is not None:
            params['origClientOrderId'] = original_client_order_id
        response = self.get('order', api_version='v3', params=params, sign=True)
        if self.debug:
            return response
        else:
            return response.json()

    def open_orders(self, symbol=None):
        params = {}
        if symbol is not None:
            params['symbol'] = symbol
        response = self.get('openOrders', api_version='v3', params=params, sign=True)
        if self.debug:
            return response
        elif self.mode == 'pandas':
            df = pd.DataFrame(response.json())
            df['timestamp'] = df['time']
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            return df
        elif self.mode == 'json':
            return response.json()

    def all_orders(self, symbol, order_id=None, limit=None):
        params = {'symbol': symbol}
        if order_id is not None:
            params['order_id'] = order_id
        if limit is not None:
            params['limit'] = limit
        response = self.get('allOrders', api_version='v3', params=params, sign=True)
        if self.debug:
            return response
        elif self.mode == 'pandas':
            df = pd.DataFrame(response.json())
            df['timestamp'] = df['time']
            df['time'] = pd.to_datetime(df['time'])
            return df
        elif self.mode == 'json':
            return response.json()

    def account_info(self):
        response = self.get('account', api_version='v3', params=None, sign=True)
        if self.debug:
            return response
        elif self.mode == 'pandas':
            data = response.json()
            df = pd.DataFrame(data['balances'])
            df['time'] = pd.to_datetime(df['timestamp'])
            return data
        elif self.mode == 'json':
            return response.json()

    def trade_list(self, symbol, limit: int = None, from_id: int = None):
        params = {'symbol': symbol}
        if limit is not None:
            params['limit'] = limit
        if from_id is not None:
            params['fromId'] = from_id
        response = self.get('myTrades', api_version='v3', params=params, sign=True)
        if self.debug:
            return response
        elif self.mode == 'pandas':
            df = pd.DataFrame(response.json())
            df['timestamp'] = df['time']
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            return df
        elif self.mode == 'json':
            return response.json()

    # endregion
