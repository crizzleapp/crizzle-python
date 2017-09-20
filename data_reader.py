import os
import time
import logging
import numpy as np
import pandas as pd
from typing import List
from os import makedirs
from os.path import exists
import exchanges
pd.set_option('display.width', 300)

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(level=logging.DEBUG)
DATA_DIR = 'data\\historical'


class DataReader:
    """
    Class that handles all data loading and fetching operations.
    You should only have one instance of this class in your bot script.
    """
    def __init__(self,
                 pairs: List[str],
                 interval: int,
                 data_dir: str,
                 exchange: str='poloniex'):
        """
        Args:
            pairs (list[str]): List of currency pairs to load
            interval (int): What sample interval to use when loading/fetching data
            data_dir (str): Disk directory where historical data resides
            exchange (str): What exchange to grab new data from
        """
        self.logger = logging.getLogger(__name__)
        self.valid_intervals = [5, 15, 30, 120, 240, 1440]
        assert interval in self.valid_intervals
        self.pairs = pairs
        self.interval = interval
        self.data_dir = os.path.join(WORKING_DIR, data_dir)
        self.exchange = exchanges.get_exchange(exchange).ExtendedAPI()

        self.dataframes = self.load_pairs_from_disk()
        self.update_all()
        # TODO: if yes, fetch new data from exchange API
        # TODO: append new data to each dataframe
        # TODO: save updated dataframes to disk
        pass

    def load_pairs_from_disk(self) -> dict:
        """
        Load the appropriate CSV file into a pandas DataFrame

        Returns:
            dict: dictionary of DataFrames {pair: dataframe}
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
                outdated.append((pair, latest))
        if outdated:
            self.logger.info("{} files require updates.".format(len(outdated)))
        else:
            self.logger.debug("No file updates required.")
        return outdated

    def _fetch_updated(self, pair, last_sample_time):
        # TODO: fetch new data from exchange
        new_data = self.exchange.get_ticker_info()
        pass

    def update_all(self):
        outdated = self.outdated
        if outdated:
            for pair in outdated:
                # TODO: fetch new data from exchange
                # TODO: update dataframe with new data
                # TODO: save dataframe to disk
                pass


def main():
    reader = DataReader(['BTC_ETH'], 5, DATA_DIR)
    print(reader.pairs)


if __name__ == '__main__':
    main()
