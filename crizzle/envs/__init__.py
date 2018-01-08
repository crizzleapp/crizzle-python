from crizzle.envs import base
from crizzle.envs import krakenex
from crizzle.envs import polonio
from crizzle.envs import shapeshiftio
from crizzle.envs import simulation


def make(exchange_name):
    exchanges = {'poloniex': polonio,
                 'kraken': krakenex,
                 'shapeshift': shapeshiftio,
                 'simulation': simulation}
    return exchanges[exchange_name].Environment()

# TODO: add aggregator functions here
