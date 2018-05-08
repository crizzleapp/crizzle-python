import os

from crizzle.envs.data_grabber import DataGrabber
from crizzle.envs.data_handler import DataHandler
from crizzle.envs import binance
from crizzle.envs import backtest


def get_data_dir():
    return os.environ['CrizzleData']


def make(name: str, *args, **kwargs):
    """
    Helper method for creating a new instance of a feed.
    Does not act as a singleton filter.

    Args:
        name: Name of the service for which to create a new feed

    Returns:

    """
    feed_map = {'binance': binance,
                'backtest': backtest}
    if name in feed_map:
        return feed_map[name].Feed(*args, **kwargs)
    else:
        raise NameError("Could not find environment with name '{}'.".format(name))
