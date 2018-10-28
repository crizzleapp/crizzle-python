import os
import time
import json
import logging
from crizzle import utils
from crizzle.feeds.base import Feed

logger = logging.getLogger(__name__)


class BinanceFeed(Feed):
    name = 'binance'

    def __init__(self, symbols: list = None, intervals: list = None):
        super(BinanceFeed, self).__init__()
        self.symbols = symbols or self.service.trading_symbols()
        self.intervals = intervals or self.constants.INTERVALS
        self.initialize_cache()

    def initialize_cache(self):
        super(BinanceFeed, self).initialize_cache()

    def get_path(self, data_type: str) -> str:
        """
        Get the path to the file where data is stored

        Returns:
            str: Name of file
        """
        return os.path.join(self.data_directory, data_type)

    def download_candlesticks(self):
        pass

    def download_historical_trades(self):
        pass

    def download_aggregated_trades(self):
        pass

    def download_all_orders(self):
        pass

    def download_my_trades(self):
        pass

    def most_recent(self) -> dict:
        """
        Checks local data directory for file existence and most recent data point for each chart

        Returns:
            dict: Dictionary of the format {interval: {symbol: latest_time}}, where latest_time is the
            timestamp of the most recent entry available, or None if there are no records for that symbol.
        """
        output = {}
        with open(self.get_path('candlestick')) as file:
            data = json.load(file)
            for interval in self.intervals:
                if interval not in output:
                    output[interval] = {}
                for symbol in self.symbols:  # TODO: fix this ugly nesting
                    if interval in data:
                        if symbol in data[interval]:
                            if len(data[interval][symbol]) > 0:
                                latest = \
                                    sorted(data[interval][symbol], key=lambda x: x['closeTimestamp'], reverse=True)[0]
                                output[interval].update({symbol: (latest['openTimestamp'], latest['closeTimestamp'])})
                            else:
                                output[interval][symbol] = (0, 0)
                        else:
                            output[interval][symbol] = (0, 0)
                    else:
                        output[interval][symbol] = (0, 0)
        return output

    def current_price_graph(self, assets=None):
        prices = self.current_price()
        trading_symbols = [sym for sym in self.service.info().json()['symbols'] if sym['status'] == 'TRADING']
        if assets:
            to_remove = []
            for sym in trading_symbols:
                if sym['baseAsset'] not in assets and sym['quoteAsset'] not in assets:
                    to_remove.append(sym)
            for sym in to_remove:
                trading_symbols.remove(sym)
        edges = list(map(
            lambda x: [x['baseAsset'], x['quoteAsset'], prices[x['baseAsset'] + x['quoteAsset']]], trading_symbols
        ))
        return utils.DiGraph(edges=edges, use_negative_log=True)

    def get_historical_candlesticks(self, interval, symbol, start=None, end=None):
        return self.service.candlesticks(symbol, interval, start=start, end=end).to_json(orient='records')

    def current_price(self, symbol=None):
        return self.service.ticker_price(symbol=symbol)

    def update_cache(self):
        """
        Brings locally stored historical data for all chosen symbols up to date.
        """
        latest_timestamps = self.most_recent()
        path = self.historical_filepath
        with open(path, 'r') as file:
            data = json.load(file)
            for interval in self.intervals:
                if interval not in data:
                    data[interval] = {}
                for symbol in self.symbols:
                    if symbol not in data[interval]:
                        data[interval][symbol] = []
                    candlesticks = data[interval][symbol]
                    open_time, close_time = latest_timestamps[interval][symbol]
                    while (time.time() * 1000) - close_time > close_time - open_time:
                        # TODO: verify out of date using a better method
                        new_candlesticks = self.service.candlesticks(symbol, interval, start=close_time)
                        open_time = new_candlesticks[-1]['openTimestamp']
                        close_time = new_candlesticks[-1]['closeTimestamp']
                        candlesticks.extend(new_candlesticks)
                        logger.debug("Interval {}; Symbol {}; Close Time {}".format(interval, symbol, close_time))
        with open(path, 'w') as file:
            json.dump(data, file, indent=2)
