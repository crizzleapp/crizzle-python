import numpy as np
import pandas as pd
np.set_printoptions()
pd.set_option('display.width', 300)

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
    return df.ix[start:start + num_rows - 1]


def cols(df, column_list):
    return df.ix[:, column_list]


def select(df, column_list, start_row=0, num_rows=None):
    if num_rows is None:
        num_rows = len(df)
    return df.ix[start_row: num_rows - 1, column_list]
# endregion


# region GENERATE DATASETS
def generate_windows(df, window_size, columns=DESIRED_COLUMNS):
    arr = np.array(select(df, columns))
    shape = (arr.shape[0] - window_size + 1, window_size) + arr.shape[1:]
    strides = (arr.strides[0],) + arr.strides
    ret = np.lib.stride_tricks.as_strided(arr, shape=shape, strides=strides)
    return ret
# endregion

if __name__ == '__main__':
    data = load_historical_data('USDT_BTC', 15)
    print(generate_windows(data, 0).shape)
    print(data.columns)
    print(generate_windows(data, 50).shape)
