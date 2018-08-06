from crizzle.services import base
from crizzle.services import binance
from crizzle.services import poloniex
from crizzle.patterns import memoize


@memoize
def make(exchange_name, *args, **kwargs):
    exchanges = {'poloniex': poloniex,
                 'binance': binance}
    return exchanges[exchange_name].BinanceService(*args, **kwargs)
