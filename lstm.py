import tensorflow as tf
import pandas as pd
import numpy as np
import random
pd.set_option('display.width', 300)


DATA_DIR = 'G:\\Documents\\Python Scripts\\Crypto_Algotrader\\data\\historical'
INTERVAL = 15  # listing interval of dataset to load

VALID_INTERVALS = [i/60 for i in [300, 900, 1800, 7200, 14400, 86400]]
assert INTERVAL in VALID_INTERVALS


# region DATA HANDLERS
def load_historical_data(pair, interval):
    assert isinstance(pair, str)
    assert interval in VALID_INTERVALS
    path = '{}\\{}\\{}.csv'.format(DATA_DIR, interval, pair)
    df = pd.read_csv(path)
    df['UTC'] = pd.to_datetime(df['UTC'])
    return df


def rows(df, start, num_rows):
    assert isinstance(df, pd.DataFrame)
    return df.ix[start:start + num_rows - 1]


def cols(df, column_list):
    assert isinstance(df, pd.DataFrame)
    assert isinstance(column_list, (list, tuple))
    return df.ix[:, column_list]
# endregion


if __name__ == '__main__':
    data = load_historical_data('USDT_BTC', 15)
    print(rows(cols(data, ['date', 'open', 'volume']), 0, 100))
    # print(data.ix[0:10, ['date', 'open', 'volume']])
