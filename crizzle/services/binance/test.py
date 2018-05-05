from unittest import TestCase
import requests
import urllib
from crizzle.services.binance import Service


env = Service(key_file="G:\\Documents\\Python Scripts\\crizzle\\data\\keys\\binance.apikey")
test_env = Service(key_file="G:\\Documents\\Python Scripts\\crizzle\\data\\keys\\binance_test.apikey")


class TestBinanceSvc(TestCase):
    def test_authenticate_request(self):
        request = requests.Request('GET', "https://api.binance.com/api/v3/order",
                                   params={'symbol': 'LTCBTC', 'side': 'BUY', 'type': 'LIMIT', 'timeInForce': 'GTC'},
                                   data={'quantity': 1, 'price': '0.1', 'recvWindow': 5000, 'timestamp': 1499827319559})
        print(urllib.parse.urlencode(request.params) + urllib.parse.urlencode(request.data))
        test_env.sign_request_data(request)
        print(request.params)
        self.failIf(request.params['signature'] != '0fd168b8ddb4876a0358a8d14d0c9f3da0e9b20c5d52b2a00fcf7d1c602f9a77')

    def test_depth(self):
        response = env.depth('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_recent_trades(self):
        response = env.recent_trades('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_historical_trades(self):
        response = env.historical_trades('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_aggregated_trades(self):
        response = env.aggregated_trades('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_candlesticks(self):
        response = env.candlesticks('ETHBTC', '1h')
        self.failIf(response.status_code != 200)

    def test_ticker_24(self):
        response = env.ticker_24('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_ticker_price(self):
        response = env.ticker_price('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_ticker_book(self):
        response = env.ticker_book('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_order(self):
        response = env.order('EOSETH', 'BUY', 'LIMIT', 5, price=0.002, time_in_force='GTC')
        print(response.content)
        self.failIf(response.status_code != 200)
        order_id = response.json()['orderId']
        response = env.query_order('EOSETH', order_id)
        self.failIf(response.status_code != 200)
        response = env.cancel_order('EOSETH', order_id)
        self.failIf(response.status_code != 200)

    def test_test_order(self):
        response = env.test_order('ETHBTC', 'BUY', 'LIMIT', 0.013, price='0.08', time_in_force='GTC')
        self.failIf(response.status_code != 200)

    def test_open_orders(self):
        response = env.open_orders('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_all_orders(self):
        response = env.all_orders('ETHBTC')
        self.failIf(response.status_code != 200)

    def test_account_info(self):
        response = env.account_info()
        self.failIf(response.status_code != 200)

    def test_trade_list(self):
        response = env.trade_list('ETHBTC')
        self.failIf(response.status_code != 200)


    def test_trading_symbols(self):
        response = env.trading_symbols()
        self.failIf(len(response) == 0)

if __name__ == '__main__':
    tester = TestBinanceSvc()
    print(tester.test_authenticate_request())
