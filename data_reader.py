import logging
import numpy as np
import pandas as pd
np.set_printoptions()
pd.set_option('display.width', 300)

logger = logging.getLogger(__name__)
DESIRED_COLUMNS = ('open', 'volume')
VALID_INTERVALS = [i/60 for i in [300, 900, 1800, 7200, 14400, 86400]]
DATA_DIR = 'G:\\Documents\\Python Scripts\\Crypto_Algotrader\\data\\historical'
INTERVAL = 15  # listing interval of dataset to load


# region DATA HANDLERS
def load_historical_data(pair, interval, columns=None):
    assert isinstance(pair, str)
    assert interval in VALID_INTERVALS
    path = '{}\\{}\\{}.csv'.format(DATA_DIR, interval, pair)
    df = pd.read_csv(path)
    df['UTC'] = pd.to_datetime(df['UTC'])
    if columns is not None:
        df = cols(df, columns)
    return df


def rows(df, start, num_rows):
    return df[start:start + num_rows - 1]


def cols(df, column_list):
    return df[column_list]


def select(df, column_list, start_row=None, num_rows=None):
    ret = cols(df, column_list)
    if num_rows is not None or start_row is not None:
        assert start_row is not None
        assert num_rows is not None
        ret = rows(ret, start_row, num_rows)
    return ret
# endregion


if __name__ == '__main__':
    data = load_historical_data('BTC_ETH', 120)
    print(select(data, ['high', 'low'], 0, 20))
    # print(data.columns)
