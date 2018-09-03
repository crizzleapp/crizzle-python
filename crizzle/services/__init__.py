from crizzle.services import base
from crizzle.services import binance
from crizzle.utils import memoize

EXCHANGE_MAP = {'binance': binance}
EXCHANGES = list(EXCHANGE_MAP.keys())


@memoize
def get(exchange_name: str, *args, **kwargs):
    exchange_name = exchange_name.lower()
    if exchange_name not in EXCHANGE_MAP:
        raise ValueError("Invalid Exchange Name '{}'".format(exchange_name))
    return EXCHANGE_MAP[exchange_name].BinanceService(*args, **kwargs)


class constants:
    binance = binance.constants
