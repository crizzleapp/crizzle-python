from crizzle.environments import base
from crizzle.environments import krakenex
from crizzle.environments import polonio
from crizzle.environments import shapeshiftio
from crizzle.environments import simulation


def make(exchange_name):
    exchanges = {'poloniex': polonio,
                 'kraken': krakenex,
                 'shapeshift': shapeshiftio,
                 'simulation': simulation}
    return exchanges[exchange_name].Environment()

# TODO: add aggregator functions here
