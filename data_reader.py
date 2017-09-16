import time
import logging
import numpy as np
import pandas as pd
from typing import List
from os import makedirs
from os.path import exists
from exchanges import polonio
pd.set_option('display.width', 300)

logging.basicConfig(level=logging.DEBUG)
# TODO: remove ^
DATA_DIR = 'G:\\Documents\\Python Scripts\\Crypto_Algotrader\\data\\historical'

# TODO: remove column and row selection functions; move them to preprocessing.


class DataReader:
    """
    Class that handles all data loading and fetching operations.
    You should only have one instance of this class in your bot script.
    """
    def __init__(self, pairs: List[str], interval: int, data_dir: str):
        """
        Args:
            pairs (list[str]): List of currency pairs to load
            interval (int): What sample interval to use when loading/fetching data
            data_dir (str): Disk directory where historical data resides
        """
        self.logger = logging.getLogger(__name__)
        self.valid_intervals = [5, 15, 30, 120, 240, 1440]
        assert interval in self.valid_intervals
        self.pairs = pairs
        self.interval = interval
        self.data_dir = data_dir

        self.dataframes = self.load_pairs_from_disk()
        # TODO: if yes, fetch new data from exchange API
        # TODO: append new data to each dataframe
        # TODO: save updated dataframes to disk
        pass

    def load_pairs_from_disk(self) -> dict:
        """
        Load the appropriate CSV file into a pandas DataFrame

        Args:
            pair (str): currency pair to load
            interval (int): sampling interval

        Returns:
            pandas.DataFrame: DataFrame containing selected features
        """
        # NOTE: Does not isolate columns
        dataframes = {}
        for pair in self.pairs:
            # TODO: try-except this bit
            assert isinstance(pair, str)
            # TODO: except AssertionError
            path = '{}\\{}\\{}.csv'.format(self.data_dir, self.interval, pair)
            dataframes[pair] = pd.read_csv(path)
            # TODO: except OSError, etc.
        return dataframes

    @property
    def outdated(self) -> list:
        """
        Checks every dataframe in self.dataframes to see if an update
        from exchange is necessary.

        Returns:
            List of currency pairs for which an update is required
        """
        outdated = []
        for pair, data in self.dataframes.items():
            dates = data['date']
            latest = dates.iloc[-1]
            now = time.time()
            if (now - latest) >= self.interval * 60:
                outdated.append(pair)
        if outdated:
            self.logger.info("{} files require updates.".format(len(outdated)))
        else:
            self.logger.debug("No file updates required.")
        return outdated

    def _fetch_updated(self, pair):
        # TODO: fetch new data from exchange
        pass

    def update_all(self):
        if self.outdated:
            for pair in self.outdated:
                # TODO: fetch new data from exchange
                # TODO: update dataframe with new data
                # TODO: save dataframe to disk
                pass


# region DATA HANDLERS
def rows(df, start, num_rows):
    return df[start:start + num_rows - 1]


def cols(df, column_list):
    return df[column_list]


def select(df, column_list, start_row=None, num_rows=None):
    """
    Select columns as well as rows

    Args:
        df (pandas.DataFrame): dataframe
        column_list (list[str]): list of columns to select
        start_row (int, optional): start row
        num_rows (optional): number of rows to select

    Returns:
        pandas.DataFrame: DataFrame containing selected columns and rows

    """
    ret = cols(df, column_list)
    if num_rows is not None or start_row is not None:
        assert start_row is not None
        assert num_rows is not None
        ret = rows(ret, start_row, num_rows)
    return ret
# endregion


if __name__ == '__main__':
    reader = DataReader(['BTC_ETH'], 30, DATA_DIR)
    print(reader.outdated)
    # print(data.columns)
