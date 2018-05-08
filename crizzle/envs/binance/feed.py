import os
import time
import json
import logging
from crizzle import patterns
from crizzle.envs.base import Feed as BaseFeed
from crizzle.services.binance import INTERVALS

logger = logging.getLogger(__name__)


class Feed(BaseFeed):
    def __init__(self, symbols: list = None, intervals: list = None, key_file: str = None):
        super(Feed, self).__init__('binance', key_file=key_file)
        self.symbols = self.service.trading_symbols() if symbols is None else symbols
        self.intervals = INTERVALS if intervals is None else intervals
        self.historical_filepath = self.filepath('historical')
        self.initialize_file(self.historical_filepath)

    def initialize_file(self, filepath: str):
        super(Feed, self).initialize_file(filepath)
        with open(filepath, 'r+') as file:
            try:
                json.load(file)
            except json.decoder.JSONDecodeError:
                file.write('{}')

    def filepath(self, data_type: str) -> str:
        """
        Get the name of the file to store the historical data in

        Returns:
            str: Name of file
        """
        return os.path.join(self.data_directory, data_type, self.name + '.json')

    def most_recent(self) -> dict:
        """
        Checks local data directory for file existence and most recent data point for each chart

        Returns:
            dict: Dictionary of the format {interval: {symbol: latest_time}}, where latest_time is the
            timestamp of the most recent entry available, or None if there are no records for that symbol.
        """
        output = {}
        with open(self.historical_filepath) as file:
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

    def current_price_graph(self):
        prices = self.current_price()
        edges = list(map(
            lambda x: [x['baseAsset'], x['quoteAsset'], prices[x['baseAsset'] + x['quoteAsset']]],
            self.service.info(key='symbols')
        ))
        return patterns.DiGraph(edges=edges)

    def get_historical_candlesticks(self, interval, symbol, start=None, end=None):
        return self.service.candlesticks(symbol, interval, start=start, end=end).to_json(orient='records')

    def current_price(self, symbol=None):
        data = self.service.ticker_price(symbol=symbol)
        if symbol is None:
            return dict(map(lambda item: (item['symbol'], float(item['price'])), data))
        else:
            return data['price']

    def update_local_historical_data(self):
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

    def next(self):
        pass
