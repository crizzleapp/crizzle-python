from . import base
from . import krakenex
from . import polonio
from . import shapeshiftio
from . import simulation


def get_environment(exchange_name):
    exchanges = {'poloniex': polonio,
                 'kraken': krakenex,
                 'shapeshift': shapeshiftio,
                 'simulation': simulation}
    return exchanges[exchange_name].Environment()
