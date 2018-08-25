import requests
from nose.tools import assert_raises
from crizzle.services.binance import BinanceService

default_timestamp = 1499827319559
unsigned_svc = BinanceService(debug=True, name='binanceunsigned', default_timestamp=default_timestamp)
svc = BinanceService(debug=True, name='binancetest', default_timestamp=default_timestamp)
svc.load_key({
    "key": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
    "secret": "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
})


def test_key_loaded():
    assert svc.key_loaded


def test_unsigned():
    assert_raises(RuntimeError, unsigned_svc.get, 'dummy', sign=True)


def test_authenticate_request():
    request = requests.Request('GET', "https://api.binance.com/api/v3/order",
                               params={'symbol': 'LTCBTC', 'side': 'BUY', 'type': 'LIMIT', 'timeInForce': 'GTC'},
                               data={'quantity': 1, 'price': '0.1', 'recvWindow': 5000,
                                     'timestamp': default_timestamp})
    svc.sign_request_data(params=request.params, data=request.data, headers=request.headers)
    assert request.params['signature'] == '0fd168b8ddb4876a0358a8d14d0c9f3da0e9b20c5d52b2a00fcf7d1c602f9a77'


def test_ping():
    response = svc.test_connection()
    assert response.url == '{}/v1/ping'.format(svc.root)
    assert response.method == 'GET'


def test_server_time():
    response = svc.server_time()
    assert response.method == 'GET'
    assert response.url == '{}/v1/time'.format(svc.root)


def test_depth_1():
    response = svc.depth('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v1/depth?symbol=ETHBTC'.format(svc.root)


def test_depth_2():
    response = svc.depth('ETHBTC', limit=100)
    assert response.method == 'GET'
    assert response.url == '{}/v1/depth?symbol=ETHBTC&limit=100'.format(svc.root)


def test_recent_trades_1():
    response = svc.recent_trades('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v1/trades?symbol=ETHBTC'.format(svc.root)


def test_recent_trades_2():
    response = svc.recent_trades('ETHBTC', limit=100)
    assert response.method == 'GET'
    assert response.url == '{}/v1/trades?symbol=ETHBTC&limit=100'.format(svc.root)


def test_historical_trades_1():
    response = svc.historical_trades('ETHBTC')
    assert response.url == '{}/v1/historicalTrades?symbol=ETHBTC'.format(svc.root)


def test_historical_trades_2():
    response = svc.historical_trades('ETHBTC', limit=100)
    assert response.url == '{}/v1/historicalTrades?symbol=ETHBTC&limit=100'.format(svc.root)


def test_historical_trades_3():
    response = svc.historical_trades('ETHBTC', from_id=12345678)
    assert response.url == '{}/v1/historicalTrades?symbol=ETHBTC&fromId=12345678'.format(svc.root)


def test_aggregated_trades_1():
    response = svc.aggregated_trades('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v1/aggTrades?symbol=ETHBTC'.format(svc.root)


def test_aggregated_trades_2():
    response = svc.aggregated_trades('ETHBTC', from_id=12345678)
    assert response.method == 'GET'
    assert response.url == '{}/v1/aggTrades?symbol=ETHBTC&fromId=12345678'.format(svc.root)


def test_aggregated_trades_3():
    response = svc.aggregated_trades('ETHBTC', limit=100)
    assert response.method == 'GET'
    assert response.url == '{}/v1/aggTrades?symbol=ETHBTC&limit=100'.format(svc.root)


def test_aggregated_trades_4():
    response = svc.aggregated_trades('ETHBTC', start=default_timestamp)
    assert response.method == 'GET'
    assert response.url == '{}/v1/aggTrades?symbol=ETHBTC&startTime={}'.format(svc.root, default_timestamp)


def test_aggregated_trades_5():
    response = svc.aggregated_trades('ETHBTC', end=default_timestamp)
    assert response.method == 'GET'
    assert response.url == '{}/v1/aggTrades?symbol=ETHBTC&endTime={}'.format(svc.root, default_timestamp)


def test_candlesticks_1():
    response = svc.candlesticks('ETHBTC', '1h')
    assert response.method == 'GET'
    assert response.url == '{}/v1/klines?symbol=ETHBTC&interval=1h'.format(svc.root)


def test_candlesticks_2():
    response = svc.candlesticks('ETHBTC', '1h', limit=100)
    assert response.method == 'GET'
    assert response.url == '{}/v1/klines?symbol=ETHBTC&interval=1h&limit=100'.format(svc.root)


def test_candlesticks_3():
    response = svc.candlesticks('ETHBTC', '1h', start=default_timestamp)
    assert response.method == 'GET'
    assert response.url == '{}/v1/klines?symbol=ETHBTC&interval=1h&startTime={}'.format(svc.root, default_timestamp)


def test_candlesticks_4():
    response = svc.candlesticks('ETHBTC', '1h', end=default_timestamp)
    assert response.method == 'GET'
    assert response.url == '{}/v1/klines?symbol=ETHBTC&interval=1h&endTime={}'.format(svc.root, default_timestamp)


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


def test_order_limit():
    response = svc.order('ETHBTC', 'BUY', 'LIMIT', 5, price=0.002, time_in_force='GTC')
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000&timeInForce=GTC&price=0.002' \
                           '&symbol=ETHBTC&type=LIMIT&quantity=5&side=BUY&signature=' \
                           '8a151667c280eb2eb1961a2fcac66f24ecec6e27302c1fd48729bc616c7f5c79'.format(svc.root)


def test_order_market():
    response = svc.order('ETHBTC', 'BUY', 'MARKET', 5, time_in_force='GTC')
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000' \
                           '&symbol=ETHBTC&type=MARKET&quantity=5&side=BUY&signature=' \
                           '13bc9bc322dfc06948ec82ef774a2fe59de0ba2e81ac9fb7f165015bfa9c9513'.format(svc.root)


def test_order_stop_loss():
    response = svc.order('ETHBTC', 'BUY', 'STOP_LOSS', 5, time_in_force='GTC', stop_price=0.002)
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000&stopPrice=0.002' \
                           '&symbol=ETHBTC&type=STOP_LOSS&quantity=5&side=BUY&signature=' \
                           '5ed2a1abc676c111afa7d2272bcdb7d1043b04de3fcbdd786969a8e67f25b5ed'.format(svc.root)


def test_order_stop_loss_limit():
    response = svc.order('ETHBTC', 'BUY', 'STOP_LOSS_LIMIT', 5, price=0.002, time_in_force='GTC', stop_price=0.0021)
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000&stopPrice=0.0021&price=0.002&' \
                           'timeInForce=GTC&symbol=ETHBTC&type=STOP_LOSS_LIMIT&quantity=5&side=BUY&signature=' \
                           '8ce7e7207bd05997dda460b7c421bd81f09f49b98bc59521674be996ba530621'.format(svc.root)


def test_order_limit_maker():
    response = svc.order('ETHBTC', 'BUY', 'LIMIT_MAKER', 5, price=0.002, time_in_force='GTC')
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000&price=0.002' \
                           '&symbol=ETHBTC&type=LIMIT_MAKER&quantity=5&side=BUY&signature=' \
                           '51fade48fa05acd8d64a0395de0829f9d5b7c20b51cfc84bed8c4d1c9ffd2d0c'.format(svc.root)


def test_order_iceberg():
    response = svc.order('ETHBTC', 'BUY', 'LIMIT', 5, price=0.002, time_in_force='GTC', iceberg_qty=3)
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000&timeInForce=GTC&price=0.002' \
                           '&icebergQty=3&symbol=ETHBTC&type=LIMIT&quantity=5&side=BUY&signature=' \
                           '9d519f6500fdfe121455ecdcaa62209f5e539a7e7b3b3978383794aa8f30bf3f'.format(svc.root)


def test_order_client_order_id():
    response = svc.order('ETHBTC', 'BUY', 'LIMIT', 5, price=0.002, time_in_force='GTC', new_client_order_id=12345678)
    assert response.method == 'POST'
    print(response.url)
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000&timeInForce=GTC&price=0.002' \
                           '&newClientOrderId=12345678&symbol=ETHBTC&type=LIMIT&quantity=5&side=BUY&signature=' \
                           '1bc4e44e37af4935bae132bd33aa296005da97322b49834eaf043c218f4385f0'.format(svc.root)


def test_order_invalid_type():
    assert_raises(ValueError, svc.order, 'ETHBTC', 'BUY', 'SOME_ORDER_TYPE', 5, price=0.002, time_in_force='GTC')


def test_test_order():
    response = svc.test_order('ETHBTC', 'BUY', 'LIMIT', 0.013, price=0.08, time_in_force='GTC')
    assert response.method == 'POST'
    assert response.url == '{}/v3/order/test?timestamp=1499827319559&recvWindow=5000&timeInForce=GTC&price=0.08' \
                           '&symbol=ETHBTC&type=LIMIT&quantity=0.013&side=BUY&signature=' \
                           'f501cd2b87a85f45601af12f7b581f2c367933d63144b1e9d712a1e0b9183db4'.format(svc.root)


def test_query_order_1():
    assert_raises(ValueError, svc.query_order, 'ETHBTC')


def test_query_order_2():
    response = svc.query_order('ETHBTC', order_id=12345678)
    assert response.method == 'GET'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000' \
                           '&symbol=ETHBTC&orderId=12345678&signature=' \
                           'c588372e8e7b62ef68a9395fd1470d6e65c82db0ec566552da35a010ea67e44f'.format(svc.root)


def test_query_order_3():
    response = svc.query_order('ETHBTC', original_client_order_id=12345678)
    assert response.method == 'GET'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000' \
                           '&symbol=ETHBTC&origClientOrderId=12345678&signature=' \
                           'e4269452dcd8e3b2ce4b09f96fe5cf35578677d053f76a90540f047b5be9302f'.format(svc.root)


def test_cancel_order_1():
    response = svc.cancel_order('ETHBTC', order_id=12345678)
    assert response.method == 'DELETE'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000' \
                           '&symbol=ETHBTC&orderId=12345678&signature=' \
                           'c588372e8e7b62ef68a9395fd1470d6e65c82db0ec566552da35a010ea67e44f'.format(svc.root)


def test_cancel_order_2():
    assert_raises(ValueError, svc.cancel_order, 'ETHBTC')


def test_cancel_order_3():
    response = svc.cancel_order('ETHBTC', original_client_order_id=12345678)
    assert response.method == 'DELETE'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000' \
                           '&symbol=ETHBTC&origClientOrderId=12345678&signature=' \
                           'e4269452dcd8e3b2ce4b09f96fe5cf35578677d053f76a90540f047b5be9302f'.format(svc.root)


def test_cancel_order_4():
    response = svc.cancel_order('ETHBTC', order_id=12345678, new_client_order_id=12345678)
    assert response.method == 'DELETE'
    assert response.url == '{}/v3/order?timestamp=1499827319559&recvWindow=5000' \
                           '&symbol=ETHBTC&orderId=12345678&newClientOrderId=12345678&signature=' \
                           'ae696312a26875f952b6fe9cebefeafc1c0fc3ee7d60ec3cd399d4f341d505cb'.format(svc.root)


def test_open_orders_1():
    response = svc.open_orders()
    assert response.url == '{}/v3/openOrders?timestamp=1499827319559&recvWindow=5000&signature=' \
                           '6cd35332399b004466463b9ad65a112a14f31fb9ddfd5e19bd7298fbd491dbc7'.format(svc.root)


def test_open_orders_2():
    response = svc.open_orders('ETHBTC')
    assert response.url == '{}/v3/openOrders?timestamp=1499827319559&recvWindow=5000&symbol=ETHBTC&signature=' \
                           'be21311f12ce93e39943125c586227c53489db5c708c9c26bc951f4da9933a7b'.format(svc.root)


def test_all_orders_1():
    response = svc.all_orders('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v3/allOrders?timestamp=1499827319559&recvWindow=5000&symbol=ETHBTC&signature=' \
                           'be21311f12ce93e39943125c586227c53489db5c708c9c26bc951f4da9933a7b'.format(svc.root)


def test_all_orders_2():
    response = svc.all_orders('ETHBTC', order_id=12345678)
    assert response.method == 'GET'
    assert response.url == '{}/v3/allOrders?timestamp=1499827319559&recvWindow=5000' \
                           '&symbol=ETHBTC&orderId=12345678&signature=' \
                           'c588372e8e7b62ef68a9395fd1470d6e65c82db0ec566552da35a010ea67e44f'.format(svc.root)


def test_all_orders_3():
    response = svc.all_orders('ETHBTC', limit=100)
    assert response.method == 'GET'
    assert response.url == '{}/v3/allOrders?timestamp=1499827319559&recvWindow=5000' \
                           '&symbol=ETHBTC&limit=100&signature=' \
                           '0ccef5fb771a9f7d5e2325e14ca5ff6931b09ed546832a04602aaf57f9eddf2b'.format(svc.root)


def test_account_info():
    response = svc.account_info()
    assert response.method == 'GET'
    assert response.url == '{}/v3/account?timestamp=1499827319559&recvWindow=5000&signature=' \
                           '6cd35332399b004466463b9ad65a112a14f31fb9ddfd5e19bd7298fbd491dbc7'.format(svc.root)


def test_trade_list_1():
    response = svc.trade_list('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v3/myTrades?timestamp=1499827319559&recvWindow=5000&symbol=ETHBTC&signature=' \
                           'be21311f12ce93e39943125c586227c53489db5c708c9c26bc951f4da9933a7b'.format(svc.root)


def test_trade_list_2():
    response = svc.trade_list('ETHBTC', limit=100)
    assert response.method == 'GET'
    assert response.url == '{}/v3/myTrades?timestamp=1499827319559&recvWindow=5000' \
                           '&symbol=ETHBTC&limit=100&signature=' \
                           '0ccef5fb771a9f7d5e2325e14ca5ff6931b09ed546832a04602aaf57f9eddf2b'.format(svc.root)


def test_trade_list_3():
    response = svc.trade_list('ETHBTC', from_id=12345678)
    assert response.method == 'GET'
    assert response.url == '{}/v3/myTrades?timestamp=1499827319559&recvWindow=5000' \
                           '&symbol=ETHBTC&fromId=12345678&signature=' \
                           '44adee218756ab394470dd86df67178e37fc67c4d2c380e1385a627f010bf0bb'.format(svc.root)


def test_trading_symbols():
    response = svc.trading_symbols()
    assert response.method == 'GET'
    assert response.url == '{}/v1/exchangeInfo'.format(svc.root)


def test_trading_assets():
    response = svc.trading_assets()
    assert response.method == 'GET'
    assert response.url == '{}/v1/exchangeInfo'.format(svc.root)
