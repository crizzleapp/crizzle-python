from crizzle.services import base
from crizzle.services import binance
from crizzle.utils import memoize

EXCHANGE_MAP = {'binance': binance,
                'poloniex': None,
                'kraken': None,
                'base': None}
EXCHANGES = list(EXCHANGE_MAP.keys())


@memoize
def get(exchange_name: str, *args, **kwargs):
    exchange_name = exchange_name.lower()
    if exchange_name not in EXCHANGE_MAP:
        raise ValueError("Invalid Exchange Name '{}'".format(exchange_name))
    module = EXCHANGE_MAP[exchange_name]
    if module is not None:
        return module.Service(*args, **kwargs)
