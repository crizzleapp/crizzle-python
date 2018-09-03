import os
from crizzle.envs import base, binance

ENVIRONMENT_MAP = {'binance': binance}
ENVIRONMENTS = list(ENVIRONMENT_MAP.keys())


def get_data_dir():
    return os.environ['CrizzleData']


def get(name: str, *args, **kwargs):
    """
    Helper method for creating a new instance of a feed.
    Does not act as a singleton filter.

    Args:
        name: Name of the service for which to create a new feed

    Returns:

    """
    if name in ENVIRONMENT_MAP:
        return ENVIRONMENT_MAP[name].BinanceFeed(*args, **kwargs)
    else:
        raise NameError("Could not find environment with name '{}'.".format(name))
