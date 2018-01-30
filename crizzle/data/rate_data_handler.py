import logging
import time
import pandas as pd
from crizzle.data.data_handler import DataHandler
from crizzle.envs.base import Environment

logger = logging.getLogger(__name__)


class RateDataHandler(DataHandler):
    """
    Base class for handlers that process exchange rate-like data
    """
    def __init__(self, data_dir=None, exchange: Environment=None):
        """
        Args:
            data_dir (str): Disk directory where historical data resides
            exchange (Environment): What exchange to grab new data from
        """
        super().__init__()
        # TODO: move next 4 lines to PoloniexDataHandler
        self._pair_intervals = {}  # loaded pair-interval combinations {pair: [interval, interval]}
        self._data_dir = data_dir
        self._exchange = exchange
        self._dataframes = {}  # nested dictionary {pair: {interval: DataFrame}}

    def handle(self, caller, state):
        pass

    # region getters and setters
    @property
    def pairs(self):
        return self._pair_intervals

    def set_exchange(self, exchange):
        try:
            assert isinstance(exchange, Environment)
        except AssertionError as e:
            logger.fatal("Provided exchange is of an incompatible type.")
            raise e
        self._exchange = exchange

    def get_data(self):
        self.update_all()
        return self._dataframes

    # endregion

    def update_pairs(self, new_pair_intervals):
        for pair in new_pair_intervals:
            if pair not in self._pair_intervals:
                self._pair_intervals[pair] = []
            for interval in new_pair_intervals[pair]:
                if interval not in self._pair_intervals[pair]:
                    self._pair_intervals[pair].append(interval)

    def update_dataframes(self, new_dataframes):
        for pair in new_dataframes:
            if pair not in self._dataframes:
                self._dataframes[pair] = {}
            for interval in new_dataframes[pair].keys():
                self._dataframes[pair][interval] = new_dataframes[pair][interval]

    def load_from_disk(self, pair_intervals: dict) -> None:
        """
        Load and store the appropriate CSV files as pandas DataFrames.

        Args:
            pair_intervals: nested dictionary of the format {pair: [interval1, interval2], pair2: [interval1]}

        Returns:
            None
        """
        try:
            assert self._data_dir is not None
        except AssertionError as e:
            logger.fatal("Data directory has not been set.")
            raise e
        try:
            for pair in pair_intervals.keys():
                assert isinstance(pair, str)
        except AssertionError as e:
            logger.fatal("Invalid pair-interval dictionary. Must be of the format {str: [int, int], str: [int,]}")
            raise e
        dataframes = {}
        for pair in pair_intervals.keys():  # for every currency pair in dict
            dataframes[pair] = {}
            for interval in pair_intervals[pair]:  # for every interval in currency pair
                path = '{}\\{}\\{}.csv'.format(self._data_dir, interval, pair)
                dataframes[pair][interval] = pd.read_csv(path)
                # TODO: except OSError, etc.
        self.update_dataframes(dataframes)
        self.update_pairs(pair_intervals)

    @property
    def outdated(self) -> list:
        """
        Checks every loaded dataframe to see if an update from exchange is necessary.

        Returns:
            List of currency pairs for which an update is required, along with the time of the most recent record.
        """
        num_loaded = 0
        outdated = []
        for pair, intervals in self._dataframes.items():
            for interval, data in intervals.items():
                num_loaded += 1
                dates = data['date']
                latest = dates.iloc[-1]
                now = time.time()
                if (now - latest) >= interval * 60:
                    outdated.append((pair, interval, latest))
        if outdated:
            logger.info("{} of {} dataframes require updates.".format(num_loaded, len(outdated)))
        else:
            logger.info("No file updates required.")
        return outdated

    def _fetch_updated(self, pair, interval, last_sample_time) -> pd.DataFrame:
        # TODO: fetch NEW (and only new) data from exchange for ONE pair-interval
        logger.debug("fetch_updated is not yet implemented")
        return pd.DataFrame()

    def update_all(self):
        outdated = self.outdated
        if outdated:
            for dfinfo in outdated:
                self._dataframes[dfinfo[0]][dfinfo[1]].append(self._fetch_updated(*dfinfo), ignore_index=True)
                pass


if __name__ == '__main__':
    def main():
        reader = RateDataHandler(data_dir="G:\\Documents\\Python Scripts\\Crypto_Algotrader\\data\\historical")
        reader.load_from_disk({'BTC_ETH': [5]})
        reader.load_from_disk({'BTC_ETH': [15]})
        reader.update_all()
        print("Currently loaded pair-interval combos: {}".format(reader.pairs))

    main()
