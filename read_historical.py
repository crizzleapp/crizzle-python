import pandas as pd
pd.set_option('display.width', 300)

DESIRED_COLUMNS = ('date', 'open', 'volume')
VALID_INTERVALS = [i/60 for i in [300, 900, 1800, 7200, 14400, 86400]]
DATA_DIR = 'G:\\Documents\\Python Scripts\\Crypto_Algotrader\\data\\historical'
INTERVAL = 15  # listing interval of dataset to load


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

def select(df, column_list, start_row, num_rows):
    return df.ix[start_row: num_rows - 1, column_list]
# endregion


# region GENERATE DATASETS
def generate_sequences(df, min_length, max_length, columns=DESIRED_COLUMNS):
    pass


if __name__ == '__main__':
    data = load_historical_data('USDT_BTC', 15)
    print(select(data, ['date', 'open', 'volume'], 0, 10))
