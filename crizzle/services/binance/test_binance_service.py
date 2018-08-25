import requests
from crizzle.services.binance import BinanceService

default_timestamp = 1499827319559
svc = BinanceService(debug=True, name='binancetest', default_timestamp=default_timestamp)
svc.load_key({
    "key": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
    "secret": "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
})


def test_key_loaded():
    assert svc.key_loaded


def test_authenticate_request():
    request = requests.Request('GET', "https://api.binance.com/api/v3/order",
                               params={'symbol': 'LTCBTC', 'side': 'BUY', 'type': 'LIMIT', 'timeInForce': 'GTC'},
                               data={'quantity': 1, 'price': '0.1', 'recvWindow': 5000,
                                     'timestamp': default_timestamp})
    svc.sign_request_data(params=request.params, data=request.data, headers=request.headers)
    assert request.params['signature'] == '0fd168b8ddb4876a0358a8d14d0c9f3da0e9b20c5d52b2a00fcf7d1c602f9a77'


def test_depth():
    response = svc.depth('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v1/depth?symbol=ETHBTC'.format(svc.root)


def test_recent_trades():
    response = svc.recent_trades('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v1/trades?symbol=ETHBTC'.format(svc.root)


def test_historical_trades():
    response = svc.historical_trades('ETHBTC')
    assert response.url == '{}/v1/historicalTrades?symbol=ETHBTC'.format(svc.root)


def test_aggregated_trades():
    response = svc.aggregated_trades('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v1/aggTrades?symbol=ETHBTC'.format(svc.root)


def test_candlesticks():
    response = svc.candlesticks('ETHBTC', '1h')
    assert response.method == 'GET'
    assert response.url == '{}/v1/klines?symbol=ETHBTC&interval=1h'.format(svc.root)


def test_ticker_24():
    response = svc.ticker_24('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v1/ticker/24hr?symbol=ETHBTC'.format(svc.root)


def test_ticker_price():
    response = svc.ticker_price('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v3/ticker/price?symbol=ETHBTC'.format(svc.root)


def test_ticker_book():
    response = svc.ticker_book('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v3/ticker/bookTicker?symbol=ETHBTC'.format(svc.root)


def test_order():
    response = svc.order('ETHBTC', 'BUY', 'LIMIT', 5, price=0.002, time_in_force='GTC')
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000&timeInForce=GTC&price=0.002' \
                           '&symbol=ETHBTC&type=LIMIT&quantity=5&side=BUY&signature=' \
                           '8a151667c280eb2eb1961a2fcac66f24ecec6e27302c1fd48729bc616c7f5c79'.format(svc.root)


def test_test_order():
    response = svc.test_order('ETHBTC', 'BUY', 'LIMIT', 0.013, price=0.08, time_in_force='GTC')
    assert response.method == 'POST'
    assert response.url == '{}/v3/order/test?timestamp=1499827319559&recvWindow=5000&timeInForce=GTC&price=0.08' \
                           '&symbol=ETHBTC&type=LIMIT&quantity=0.013&side=BUY&signature=' \
                           'f501cd2b87a85f45601af12f7b581f2c367933d63144b1e9d712a1e0b9183db4'.format(svc.root)


def test_cancel_order():
    response = svc.cancel_order('ETHBTC', 12345678)
    assert response.method == 'DELETE'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000' \
                           '&symbol=ETHBTC&orderId=12345678&signature=' \
                           'c588372e8e7b62ef68a9395fd1470d6e65c82db0ec566552da35a010ea67e44f'.format(svc.root)


def test_open_orders():
    response = svc.open_orders('ETHBTC')
    assert response.url == '{}/v3/openOrders?timestamp=1499827319559&recvWindow=5000&symbol=ETHBTC&signature=' \
                           'be21311f12ce93e39943125c586227c53489db5c708c9c26bc951f4da9933a7b'.format(svc.root)


def test_all_orders():
    response = svc.all_orders('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v3/allOrders?timestamp=1499827319559&recvWindow=5000&symbol=ETHBTC&signature=' \
                           'be21311f12ce93e39943125c586227c53489db5c708c9c26bc951f4da9933a7b'.format(svc.root)


def test_account_info():
    response = svc.account_info()
    assert response.method == 'GET'
    assert response.url == '{}/v3/account?timestamp=1499827319559&recvWindow=5000&signature=' \
                           '6cd35332399b004466463b9ad65a112a14f31fb9ddfd5e19bd7298fbd491dbc7'.format(svc.root)


def test_trade_list():
    response = svc.trade_list('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v3/myTrades?timestamp=1499827319559&recvWindow=5000&symbol=ETHBTC&signature=' \
                           'be21311f12ce93e39943125c586227c53489db5c708c9c26bc951f4da9933a7b'.format(svc.root)


def test_trading_symbols():
    response = svc.trading_symbols()
    assert response.method == 'GET'
    assert response.url == '{}/v1/exchangeInfo'.format(svc.root)
