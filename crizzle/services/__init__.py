from crizzle.patterns import memoize
from crizzle.services import poloniex
from crizzle.services import binance


@memoize
def make(exchange_name, *args, **kwargs):
    exchanges = {'poloniex': poloniex,
                 'binance': binance}
    return exchanges[exchange_name].Service(*args, **kwargs)
