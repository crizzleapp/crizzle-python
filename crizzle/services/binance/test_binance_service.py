import requests
from nose.tools import assert_raises
import crizzle
from crizzle.services.binance import BinanceService

default_timestamp = 1499827319559
unsigned_svc = BinanceService(debug=True, name='binanceunsigned', default_timestamp=default_timestamp)
svc = BinanceService(debug=True, name='binancetest', default_timestamp=default_timestamp)
crizzle.set_service_key('binancetest',
                        {
                            "key": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
                            "secret": "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
                        })


def test_key_loaded():
    assert svc.key_loaded


def test_unsigned():
    assert_raises(RuntimeError, unsigned_svc.get, 'dummy', sign=True)


def test_sort_params():
    params = {'symbol': 'LTCBTC', 'side': 'BUY', 'type': 'LIMIT', 'timeInForce': 'GTC', '123': 'value'}
    sorted_params = svc.sort_dict(params)
    assert list(sorted_params.keys()) == ['123', 'side', 'symbol', 'timeInForce', 'type']
    assert list(sorted_params.values()) == ['value', 'BUY', 'LTCBTC', 'GTC', 'LIMIT']


def test_authenticate_request():
    params = {'symbol': 'LTCBTC', 'side': 'BUY', 'type': 'LIMIT', 'timeInForce': 'GTC'}
    data = {'quantity': 1, 'price': '0.1', 'recvWindow': 5000, 'timestamp': default_timestamp}
    params = svc.sort_dict(params)
    data = svc.sort_dict(data)
    request = requests.Request('GET', "https://api.binance.com/api/v3/order",
                               params=params, data=data)
    svc.sign_request_data(params=request.params, data=request.data, headers=request.headers)
    assert request.params['signature'] == '11e806e5291154e36ffd93622440cc230663129f67878ccc1a7385011df29ee2'


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
    assert response.url == '{}/v1/depth?limit=100&symbol=ETHBTC'.format(svc.root)


def test_recent_trades_1():
    response = svc.recent_trades('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v1/trades?symbol=ETHBTC'.format(svc.root)


def test_recent_trades_2():
    response = svc.recent_trades('ETHBTC', limit=100)
    assert response.method == 'GET'
    assert response.url == '{}/v1/trades?limit=100&symbol=ETHBTC'.format(svc.root)


def test_historical_trades_1():
    response = svc.historical_trades('ETHBTC')
    assert response.url == '{}/v1/historicalTrades?symbol=ETHBTC'.format(svc.root)


def test_historical_trades_2():
    response = svc.historical_trades('ETHBTC', limit=100)
    assert response.url == '{}/v1/historicalTrades?limit=100&symbol=ETHBTC'.format(svc.root)


def test_historical_trades_3():
    response = svc.historical_trades('ETHBTC', from_id=12345678)
    assert response.url == '{}/v1/historicalTrades?fromId=12345678&symbol=ETHBTC'.format(svc.root)


def test_aggregated_trades_1():
    response = svc.aggregated_trades('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v1/aggTrades?symbol=ETHBTC'.format(svc.root)


def test_aggregated_trades_2():
    response = svc.aggregated_trades('ETHBTC', from_id=12345678)
    assert response.method == 'GET'
    assert response.url == '{}/v1/aggTrades?fromId=12345678&symbol=ETHBTC'.format(svc.root)


def test_aggregated_trades_3():
    response = svc.aggregated_trades('ETHBTC', limit=100)
    assert response.method == 'GET'
    assert response.url == '{}/v1/aggTrades?limit=100&symbol=ETHBTC'.format(svc.root)


def test_aggregated_trades_4():
    response = svc.aggregated_trades('ETHBTC', start=default_timestamp)
    assert response.method == 'GET'
    assert response.url == '{}/v1/aggTrades?startTime={}&symbol=ETHBTC'.format(svc.root, default_timestamp)


def test_aggregated_trades_5():
    response = svc.aggregated_trades('ETHBTC', end=default_timestamp)
    assert response.method == 'GET'
    assert response.url == '{}/v1/aggTrades?endTime={}&symbol=ETHBTC'.format(svc.root, default_timestamp)


def test_candlesticks_1():
    response = svc.candlesticks('ETHBTC', '1h')
    assert response.method == 'GET'
    assert response.url == '{}/v1/klines?interval=1h&symbol=ETHBTC'.format(svc.root)


def test_candlesticks_2():
    response = svc.candlesticks('ETHBTC', '1h', limit=100)
    assert response.method == 'GET'
    assert response.url == '{}/v1/klines?interval=1h&limit=100&symbol=ETHBTC'.format(svc.root)


def test_candlesticks_3():
    response = svc.candlesticks('ETHBTC', '1h', start=default_timestamp)
    assert response.method == 'GET'
    assert response.url == '{}/v1/klines?interval=1h&startTime={}&symbol=ETHBTC'.format(svc.root, default_timestamp)


def test_candlesticks_4():
    response = svc.candlesticks('ETHBTC', '1h', end=default_timestamp)
    assert response.method == 'GET'
    assert response.url == '{}/v1/klines?endTime={}&interval=1h&symbol=ETHBTC'.format(svc.root, default_timestamp)


def test_ticker_24():
    response = svc.ticker_24('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v1/ticker/24hr?symbol=ETHBTC'.format(svc.root)


def test_ticker_price():
    response = svc.ticker_price('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v3/ticker/price'.format(svc.root)


def test_ticker_book():
    response = svc.ticker_book('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v3/ticker/bookTicker?symbol=ETHBTC'.format(svc.root)


def test_order_limit():
    response = svc.order('ETHBTC', 'BUY', 'LIMIT', 5, price=0.002, time_in_force='GTC')
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?newOrderRespType=FULL&price=0.002&quantity=5&recvWindow=5000&side=BUY' \
                           '&symbol=ETHBTC&timeInForce=GTC&timestamp=1499827319559&type=LIMIT&signature=' \
                           '52c9955ee471879351cdc76a0fc9c56c87345da9e7417747c4387e800e3dc74a'.format(svc.root)


def test_order_market():
    response = svc.order('ETHBTC', 'BUY', 'MARKET', 5, time_in_force='GTC')
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?newOrderRespType=FULL&quantity=5&recvWindow=5000&side=BUY' \
                           '&symbol=ETHBTC&timestamp=1499827319559&type=MARKET&signature=' \
                           'd168615a4bf2674924c99fb37795b4e284d7f5e5923a70b9bf501d0edc0764ae'.format(svc.root)


def test_order_stop_loss():
    response = svc.order('ETHBTC', 'BUY', 'STOP_LOSS', 5, time_in_force='GTC', stop_price=0.002)
    assert response.method == 'POST'

    assert response.url == '{}/v3/order?newOrderRespType=FULL&quantity=5&recvWindow=5000&side=BUY' \
                           '&stopPrice=0.002&symbol=ETHBTC&timestamp=1499827319559&type=STOP_LOSS&signature=' \
                           'db0d09de4de3019133544d6ae6ef2f65a53bc9d8827137538636bf6b6105ef34'.format(svc.root)


def test_order_stop_loss_limit():
    response = svc.order('ETHBTC', 'BUY', 'STOP_LOSS_LIMIT', 5, price=0.002, time_in_force='GTC', stop_price=0.0021)
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?newOrderRespType=FULL&price=0.002&quantity=5&recvWindow=5000&side=BUY' \
                           '&stopPrice=0.0021&symbol=ETHBTC&timeInForce=GTC' \
                           '&timestamp=1499827319559&type=STOP_LOSS_LIMIT&signature=' \
                           '9bba0bfed1c85c89184d49f9b870e7a722d0147c78fb2f38a0845ff3e2b4ef84'.format(svc.root)


def test_order_limit_maker():
    response = svc.order('ETHBTC', 'BUY', 'LIMIT_MAKER', 5, price=0.002, time_in_force='GTC')
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?newOrderRespType=FULL&price=0.002&quantity=5&recvWindow=5000&side=BUY' \
                           '&symbol=ETHBTC&timestamp=1499827319559&type=LIMIT_MAKER&signature=' \
                           '73bb89d6ea0f8424b24902dc56f378718a17327b24f4f816f6d10c97d53e7f9c'.format(svc.root)


def test_order_iceberg():
    response = svc.order('ETHBTC', 'BUY', 'LIMIT', 5, price=0.002, time_in_force='GTC', iceberg_qty=3)
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?icebergQty=3&newOrderRespType=FULL&price=0.002&quantity=5&recvWindow=5000' \
                           '&side=BUY&symbol=ETHBTC&timeInForce=GTC&timestamp=1499827319559&type=LIMIT&signature=' \
                           '720bbc52e864b338386e76e403a250f69c44c41709263af482afde0dcb305a6c'.format(svc.root)


def test_order_client_order_id():
    response = svc.order('ETHBTC', 'BUY', 'LIMIT', 5, price=0.002, time_in_force='GTC', new_client_order_id=12345678)
    assert response.method == 'POST'
    assert response.url == '{}/v3/order?newClientOrderId=12345678&newOrderRespType=FULL&price=0.002' \
                           '&quantity=5&recvWindow=5000&side=BUY&symbol=ETHBTC' \
                           '&timeInForce=GTC&timestamp=1499827319559&type=LIMIT&signature=' \
                           'f20ef32ba8a9c248dcf384380a64e157f56ef79c61bc4c5e949e00dff1a841f0'.format(svc.root)


def test_order_invalid_type():
    assert_raises(ValueError, svc.order, 'ETHBTC', 'BUY', 'SOME_ORDER_TYPE', 5, price=0.002, time_in_force='GTC')


def test_test_order():
    response = svc.test_order('ETHBTC', 'BUY', 'LIMIT', 0.013, price=0.08, time_in_force='GTC')
    assert response.method == 'POST'
    assert response.url == '{}/v3/order/test?newOrderRespType=FULL&price=0.08&quantity=0.013&recvWindow=5000' \
                           '&side=BUY&symbol=ETHBTC&timeInForce=GTC&timestamp=1499827319559&type=LIMIT&signature=' \
                           '9ed118dd9bbc6a8fe127183321bef4ee8980d85496a3962ebd795d7a73be715f'.format(svc.root)


def test_query_order_1():
    assert_raises(ValueError, svc.query_order, 'ETHBTC')


def test_query_order_2():
    response = svc.query_order('ETHBTC', order_id=12345678)
    assert response.method == 'GET'
    assert response.url == '{}/v3/order?orderId=12345678&recvWindow=5000' \
                           '&symbol=ETHBTC&timestamp=1499827319559&signature=' \
                           '18ea3e337d0e8a38e0617672eb4c7de9afe95fdb5da64ab834248fb46c69c26f'.format(svc.root)


def test_query_order_3():
    response = svc.query_order('ETHBTC', original_client_order_id=12345678)
    assert response.method == 'GET'
    assert response.url == '{}/v3/order?origClientOrderId=12345678&recvWindow=5000' \
                           '&symbol=ETHBTC&timestamp=1499827319559&signature=' \
                           '47b48a8048df0a1e59a9f391cda9258bb4cf5c9c3374f11da77753b8d5afe447'.format(svc.root)


def test_cancel_order_1():
    response = svc.cancel_order('ETHBTC', order_id=12345678)
    assert response.method == 'DELETE'
    assert response.url == '{}/v3/order?orderId=12345678&recvWindow=5000' \
                           '&symbol=ETHBTC&timestamp=1499827319559&signature=' \
                           '18ea3e337d0e8a38e0617672eb4c7de9afe95fdb5da64ab834248fb46c69c26f'.format(svc.root)


def test_cancel_order_2():
    assert_raises(ValueError, svc.cancel_order, 'ETHBTC')


def test_cancel_order_3():
    response = svc.cancel_order('ETHBTC', original_client_order_id=12345678)
    assert response.method == 'DELETE'
    assert response.url == '{}/v3/order?origClientOrderId=12345678&recvWindow=5000' \
                           '&symbol=ETHBTC&timestamp=1499827319559&signature=' \
                           '47b48a8048df0a1e59a9f391cda9258bb4cf5c9c3374f11da77753b8d5afe447'.format(svc.root)


def test_cancel_order_4():
    response = svc.cancel_order('ETHBTC', order_id=12345678, new_client_order_id=12345678)
    assert response.method == 'DELETE'
    assert response.url == '{}/v3/order?newClientOrderId=12345678&orderId=12345678' \
                           '&recvWindow=5000&symbol=ETHBTC&timestamp=1499827319559&signature=' \
                           '106021926025bf64a2a0c97cd61e33f6d131367a28035e0a54d078598addd5f0'.format(svc.root)


def test_open_orders_1():
    response = svc.open_orders()
    assert response.url == '{}/v3/openOrders?recvWindow=5000&timestamp=1499827319559&signature=' \
                           '82f4e72e95e63d666b6da651e82a701722ad8a785a169318d91f36f279c55821'.format(svc.root)


def test_open_orders_2():
    response = svc.open_orders('ETHBTC')
    assert response.url == '{}/v3/openOrders?recvWindow=5000' \
                           '&symbol=ETHBTC&timestamp=1499827319559&signature=' \
                           'afc235c64e5abb3fa25ab4dfbaad6a8c655eefa3689ac63b5ef88bf04882c7c6'.format(svc.root)


def test_all_orders_1():
    response = svc.all_orders('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v3/allOrders?recvWindow=5000&symbol=ETHBTC&timestamp=1499827319559&signature=' \
                           'afc235c64e5abb3fa25ab4dfbaad6a8c655eefa3689ac63b5ef88bf04882c7c6'.format(svc.root)


def test_all_orders_2():
    response = svc.all_orders('ETHBTC', order_id=12345678)
    assert response.method == 'GET'
    assert response.url == '{}/v3/allOrders?orderId=12345678&recvWindow=5000' \
                           '&symbol=ETHBTC&timestamp=1499827319559&signature=' \
                           '18ea3e337d0e8a38e0617672eb4c7de9afe95fdb5da64ab834248fb46c69c26f'.format(svc.root)


def test_all_orders_3():
    response = svc.all_orders('ETHBTC', limit=100)
    assert response.method == 'GET'
    assert response.url == '{}/v3/allOrders?limit=100&recvWindow=5000' \
                           '&symbol=ETHBTC&timestamp=1499827319559&signature=' \
                           '7f100e10826872aa87fb7f9060db1e17b10785874a2a66d9e84810d8c42d10d8'.format(svc.root)


def test_account_info():
    response = svc.account_info()
    assert response.method == 'GET'
    assert response.url == '{}/v3/account?recvWindow=5000&timestamp=1499827319559&signature=' \
                           '82f4e72e95e63d666b6da651e82a701722ad8a785a169318d91f36f279c55821'.format(svc.root)


def test_trade_list_1():
    response = svc.my_trades('ETHBTC')
    assert response.method == 'GET'
    assert response.url == '{}/v3/myTrades?recvWindow=5000&symbol=ETHBTC&timestamp=1499827319559&signature=' \
                           'afc235c64e5abb3fa25ab4dfbaad6a8c655eefa3689ac63b5ef88bf04882c7c6'.format(svc.root)


def test_trade_list_2():
    response = svc.my_trades('ETHBTC', limit=100)
    assert response.method == 'GET'
    assert response.url == '{}/v3/myTrades?limit=100&recvWindow=5000&symbol=ETHBTC&timestamp=1499827319559&signature=' \
                           '7f100e10826872aa87fb7f9060db1e17b10785874a2a66d9e84810d8c42d10d8'.format(svc.root)


def test_trade_list_3():
    response = svc.my_trades('ETHBTC', from_id=12345678)
    assert response.method == 'GET'
    assert response.url == '{}/v3/myTrades?fromId=12345678&recvWindow=5000' \
                           '&symbol=ETHBTC&timestamp=1499827319559&signature=' \
                           '22919c5936680b807651bdb9f800aa38e055e6915e841853c9db7fb35d474334'.format(svc.root)


def test_trading_symbols():
    response = svc.trading_symbols()
    assert response.method == 'GET'
    assert response.url == '{}/v1/exchangeInfo'.format(svc.root)


def test_trading_assets():
    response = svc.trading_assets()
    assert response.method == 'GET'
    assert response.url == '{}/v1/exchangeInfo'.format(svc.root)
