import os
from crizzle.environments.data_grabber import DataGrabber
from crizzle.environments.data_handler import DataHandler
from crizzle.environments import binance
from crizzle.environments import backtest

dir_file = os.path.join(os.path.dirname(__file__), 'local_data_directory.txt')
with open(dir_file, 'r') as file:
    local_directory = file.read()


def set_local_data_dir(local_dir: str):
    try:
        with open(dir_file, 'w') as file:
            file.write(local_dir)
    except IOError as e:
        # TODO: more elegant error handling?
        raise e


def get_local_data_dir():
    with open(dir_file, 'r') as file:
        return file.read()


def make_feed(name: str, local_dir: str, *args, **kwargs):
    feed_map = {'binance': binance,
                'backtest': backtest}
    if name in feed_map:
        return feed_map[name].Feed(local_dir, *args, **kwargs)
    else:
        raise NameError("Could not find environment with name '{}'.".format(name))


if __name__ == '__main__':
    print(get_local_data_dir())
    set_local_data_dir(get_local_data_dir() + 'x')
    print(get_local_data_dir())
