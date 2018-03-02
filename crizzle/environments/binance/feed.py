import os
import json
import logging
from crizzle.environments.base import Feed as BaseFeed
from crizzle.services.binance import INTERVALS

logger = logging.getLogger(__name__)


class Feed(BaseFeed):
    def __init__(self, symbols: list, key_file: str=None):
        super(Feed, self).__init__('binance', key_file=key_file)
        self.all_symbols = self.service.trading_symbols()
        self.symbols = symbols
        self.intervals = INTERVALS
        self.files = self.get_filenames(self.symbols, self.intervals)
        self.create_nonexistent_files(self.files)

    def get_filenames(self, symbols: list, intervals: list) -> dict:
        """Get the folder structure to store local data in, given the symbols and intervals to store

        Args:
            symbols (list): List of symbols to include in the folder structure
            intervals (list): List of intervals to include for each symbol

        Returns:
            dict: Dictionary representation of the folder structure, in the format {symbol: [intervals...]}
        """
        # TODO: store as CSV instead of JSON
        output = {}
        for symbol in symbols:
            output[symbol] = []
            for interval in intervals:
                output[symbol].append('{}.json'.format(interval))
        return output

    def get_filepath(self, symbol: str, interval: str) -> str:
        return os.path.join(self.data_directory, symbol, '{}.json'.format(interval))

    def check_local_data(self) -> dict:
        """
        Checks local data directory for file existence and most recent datapoint for each data type

        Returns:
            dict: Dictionary of the format {symbol: {interval: latest_time}}, where latest_time is the
            timestamp of the most recent entry in the file, or None if the file is empty.
        """
        output = {}
        for symbol in self.symbols:
            if symbol not in output:
                output[symbol] = {}
            for interval in self.intervals:
                path = self.get_filepath(symbol, interval)
                with open(path) as file:
                    try:
                        data = json.load(file)
                        last_close_time = data[-1][6]
                        print()
                    except json.JSONDecodeError:
                        # TODO: replace with CSV/pandas error checking
                        last_close_time = 0
                        logger.info("Error decoding file {}, it may be malformed or empty.".format(path))
                output[symbol][interval] = last_close_time
        return output

    def get_historical_candlesticks(self, symbol, interval, start=None, end=None):
        return self.service.candlesticks(symbol, interval, start=start, end=end)

    def update_local_historical_data(self, symbol: str, data_type: str):
        """
        Updates local candlestick data.

        Args:
            symbol:
            data_type:

        Returns:

        """
        pass

    def next(self):
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    key = 'G:\\Documents\\Python Scripts\\crizzle\\data\\keys\\binance.apikey'
    feed = Feed(['TRXETH', 'EOSETH'], key_file=key)
    print(feed.check_local_data())
