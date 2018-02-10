"""Given a list of currencies, fetch and save all
historical data for each one to disk at given interval"""

import logging
from os import makedirs
from os.path import exists

import pandas as pd

pd.set_option('display.width', 300)

DATA_DIR = "G:\\Documents\\Python Scripts\\Crypto_Algotrader\\data"

logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
exchange = polonio.Environment()


def get_all_currency_pairs():
    return exchange.return_ticker().keys()


def get_historical_data(currency_pair, interval):
    """
    Return historical data from exchange for a given currency pair
    """
    logger.info('fetching historical data for {}'.format(currency_pair))
    b = exchange.return_chart_data(currency_pair, interval=interval, start=0, end=9999999999)
    return b


def data_to_df(data):
    """Return Pandas DataFrame object containing historical data"""
    assert isinstance(data, (list, dict, tuple))
    df = pd.DataFrame(data)
    df.insert(0, 'UTC', pd.to_datetime(df['date'], unit='s'))
    cols = ['UTC', 'date', 'open', 'high', 'low', 'close',
            'quoteVolume', 'volume', 'weightedAverage']
    df = df[cols]
    return df


def save_df(df, name, interval, compress=False):
    """Save a dataframe with the given name in /data"""
    assert isinstance(df, pd.DataFrame)
    compress = None if not compress else 'gzip'
    path = '{}\\{}'.format(DATA_DIR, int(interval//60))
    if not exists(path):
        makedirs(path)
    path += '\\{}.csv'.format(name)
    if compress == 'gzip':
        path += '.gz'

    logger.debug('saving {} to {}'.format(name, path))
    df.to_csv(path, index=False, compression=compress)


def fetch_history(currency_pair, interval, compress=False):
    """Save and return the full history of a given currency pair"""
    data = get_historical_data(currency_pair, interval)
    hist = data_to_df(data)
    save_df(hist, currency_pair, interval, compress=compress)
    return hist


def fetch_histories(currency_pairs, interval, compress=False):
    assert isinstance(currency_pairs, (list, tuple))
    for pair_name in currency_pairs:
        fetch_history(pair_name, interval, compress=compress)


if __name__ == '__main__':
    CURRENCY_PAIRS = list(get_all_currency_pairs())
    for i in reversed([300, 900, 1800, 7200, 14400, 86400]):
        fetch_histories(CURRENCY_PAIRS, i, compress=False)
