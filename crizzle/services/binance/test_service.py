from unittest import TestCase
import requests
import urllib
from crizzle.services.binance import Service


svc = Service(key_file="G:\\Documents\\Python Scripts\\crizzle\\data\\keys\\binance.apikey", debug=True)
test_svc = Service(key_file="G:\\Documents\\Python Scripts\\crizzle\\data\\keys\\binance_test.apikey", debug=True)


class TestBinanceSvc(TestCase):
    def test_authenticate_request(self):
        request = requests.Request('GET', "https://api.binance.com/api/v3/order",
                                   params={'symbol': 'LTCBTC', 'side': 'BUY', 'type': 'LIMIT', 'timeInForce': 'GTC'},
                                   data={'quantity': 1, 'price': '0.1', 'recvWindow': 5000, 'timestamp': 1499827319559})
        test_svc.sign_request_data(params=request.params, data=request.data, headers=request.headers)
        self.failIf(request.params['signature'] != '0fd168b8ddb4876a0358a8d14d0c9f3da0e9b20c5d52b2a00fcf7d1c602f9a77')

    def test_depth(self):
        response = svc.depth('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_recent_trades(self):
        response = svc.recent_trades('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_historical_trades(self):
        response = svc.historical_trades('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_aggregated_trades(self):
        response = svc.aggregated_trades('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_candlesticks(self):
        response = svc.candlesticks('ETHBTC', '1h')
        self.failIf(response.status_code != 200)

    def test_ticker_24(self):
        response = svc.ticker_24('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_ticker_price(self):
        response = svc.ticker_price('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_ticker_book(self):
        response = svc.ticker_book('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_order(self):
        response = svc.order('EOSETH', 'BUY', 'LIMIT', 5, price=0.002, time_in_force='GTC')
        print(response.content)
        self.failIf(response.status_code != 200)
        order_id = response.json()['orderId']
        response = svc.query_order('EOSETH', order_id)
        self.failIf(response.status_code != 200)
        response = svc.cancel_order('EOSETH', order_id)
        self.failIf(response.status_code != 200)

    def test_test_order(self):
        response = svc.test_order('ETHBTC', 'BUY', 'LIMIT', 0.013, price='0.08', time_in_force='GTC')
        self.failIf(response.status_code != 200)

    def test_open_orders(self):
        response = svc.open_orders('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_all_orders(self):
        response = svc.all_orders('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_account_info(self):
        response = svc.account_info()
        self.failIf(response.status_code != 200)

    def test_trade_list(self):
        response = svc.trade_list('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_trading_symbols(self):
        response = svc.trading_symbols()
        self.failIf(len(response) == 0)
