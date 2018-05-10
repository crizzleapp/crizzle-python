import os
import requests

from crizzle.services.binance import Service
from crizzle import load_key

svc = Service(debug=True)
test_svc = Service(key={
    "key": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
    "secret": "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
}, debug=True)


def test_key_loaded():
    assert test_svc.key_loaded
    if 'CrizzleKey_binance' not in os.environ:
        load_key('G:\\Documents\\CrizzleData\\keys\\binance.json')
    assert svc.key_loaded


def test_authenticate_request():
    request = requests.Request('GET', "https://api.binance.com/api/v3/order",
                               params={'symbol': 'LTCBTC', 'side': 'BUY', 'type': 'LIMIT', 'timeInForce': 'GTC'},
                               data={'quantity': 1, 'price': '0.1', 'recvWindow': 5000, 'timestamp': 1499827319559})
    test_svc.sign_request_data(params=request.params, data=request.data, headers=request.headers)
    assert request.params['signature'] == '0fd168b8ddb4876a0358a8d14d0c9f3da0e9b20c5d52b2a00fcf7d1c602f9a77'


def test_depth():
    response = svc.depth('ETHBTC')
    assert response.status_code == 200


def test_recent_trades():
    response = svc.recent_trades('ETHBTC')
    assert response.status_code == 200


def test_historical_trades():
    response = svc.historical_trades('ETHBTC')
    assert response.status_code == 200


def test_aggregated_trades():
    response = svc.aggregated_trades('ETHBTC')
    assert response.status_code == 200


def test_candlesticks():
    response = svc.candlesticks('ETHBTC', '1h')
    assert response.status_code == 200


def test_ticker_24():
    response = svc.ticker_24('ETHBTC')
    assert response.status_code == 200


def test_ticker_price():
    response = svc.ticker_price('ETHBTC')
    assert response.status_code == 200


def test_ticker_book():
    response = svc.ticker_book('ETHBTC')
    assert response.status_code == 200


def test_order():
    response = svc.order('EOSETH', 'BUY', 'LIMIT', 5, price=0.002, time_in_force='GTC')
    print(response.content)
    assert response.status_code == 200
    order_id = response.json()['orderId']
    response = svc.query_order('EOSETH', order_id)
    assert response.status_code == 200
    response = svc.cancel_order('EOSETH', order_id)
    assert response.status_code == 200


def test_test_order():
    response = svc.test_order('ETHBTC', 'BUY', 'LIMIT', 0.013, price='0.08', time_in_force='GTC')
    assert response.status_code == 200


def test_open_orders():
    response = svc.open_orders('ETHBTC')
    assert response.status_code == 200


def test_all_orders():
    response = svc.all_orders('ETHBTC')
    assert response.status_code == 200


def test_account_info():
    response = svc.account_info()
    assert response.status_code == 200


def test_trade_list():
    response = svc.trade_list('ETHBTC')
    assert response.status_code == 200


def test_trading_symbols():
    response = svc.trading_symbols()
    assert len(response) == 0
