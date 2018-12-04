import re
import logging
from contextlib import contextmanager
from crizzle import utils
from crizzle.utils import database
from crizzle.feeds.base import Feed
from concurrent.futures import as_completed
from collections import OrderedDict
from tqdm import tqdm

MAX_CANDLES_PER_REQUEST = 1000


class BinanceFeed(Feed):
    def __init__(self, symbols: list = None, name: str = None):
        super(BinanceFeed, self).__init__('binance', name=name)
        self.symbols = symbols or self.service.trading_symbols()
        self.intervals = self.constants.INTERVALS
        self.initialise_db()

    @contextmanager
    def connection(self):
        with self.db.transaction() as conn:
            yield conn
            conn.close()

    def initialise_db(self):
        with self.db.transaction() as conn:
            if 'candlestick_collection' not in conn.root():
                candlestick_collection = database.CandlestickCollection()
                conn.root.candlestick_collection = candlestick_collection
            candlestick_collection = conn.root.candlestick_collection
            for interval in self.intervals:
                for symbol in self.symbols:
                    if (interval, symbol) not in candlestick_collection:
                        candlestick_collection[interval, symbol] = utils.database.Candlesticks()
                    elif not isinstance(candlestick_collection[interval, symbol], utils.database.Candlesticks):
                        candlestick_collection[interval, symbol] = utils.database.Candlesticks()

    def _get_symbols(self, symbol_patterns=None):
        if symbol_patterns is None:
            return self.symbols
        symbols = set()
        for symbol_pattern in symbol_patterns:
            pattern = re.compile(symbol_pattern)
            symbols.update(filter(pattern.match, self.symbols))
        return list(symbols)

    def _fetch_candlesticks(self, inter, sym, start):
        incoming = self.service.candlesticks(sym, inter, start=start, limit=MAX_CANDLES_PER_REQUEST).json()
        new_candlesticks = {i[0]: utils.database.Candlestick(
            i[0],
            *i[1:5],
            volume=i[5],
            quote_volume=i[7],
            close_timestamp=i[6]
        ) for i in incoming}
        return new_candlesticks, inter, sym

    def _get_update_timestamps(self, intervals=None, symbols=None):
        symbols = self._get_symbols(symbols)
        intervals = intervals or self.intervals

        def get_first_timestamp(inter, sym):
            result = self.service.candlesticks(sym, inter, limit=1, start=0)
            return result.json()[0][0]

        symbols = symbols or self.symbols
        with self.db.transaction() as conn:
            start_timestamps = OrderedDict()
            empty = []
            for interval in reversed(sorted(intervals)):
                for symbol in symbols:
                    candlesticks = conn.root.candlestick_collection[interval, symbol]
                    latest = candlesticks.most_recent()
                    inter_time = self.constants.interval_value(interval)
                    if (self.time - latest) > inter_time:  # requires update
                        if latest == 0:
                            empty.append((interval, symbol))
                        else:
                            start_timestamps[(interval, symbol)] = latest
            with self._threads() as tpe:
                first_timestamps = OrderedDict()
                for interval, symbol in empty:
                    first_timestamps[tpe.submit(get_first_timestamp, interval, symbol)] = (interval, symbol)
                if first_timestamps:
                    with tqdm(total=len(first_timestamps), unit='requests', ncols=100,
                              desc="Initial timestamps") as pbar:
                        for future in as_completed(first_timestamps):
                            start_timestamps[first_timestamps[future]] = future.result()
                            pbar.update(1)
                tpe.shutdown(wait=True)
        jobs = []
        for (interval, symbol), start in start_timestamps.items():
            for timestamp in range(start,
                                   int(round(self.time)),
                                   self.constants.interval_value(interval) * MAX_CANDLES_PER_REQUEST):
                jobs.append((interval, symbol, timestamp))
        return jobs

    def download_candlesticks(self, intervals=None, min_interval_seconds=900, symbols=None):
        symbols = self._get_symbols(symbols)
        if intervals is None:
            intervals = [i for i in self.intervals if
                         self.constants.interval_value(i) > min_interval_seconds * self.time_multiplier]

        timestamps = self._get_update_timestamps(intervals=intervals, symbols=symbols)
        # print(timestamps)
        with self.db.transaction() as connection:
            with self._threads() as executor:
                futures_to_params = [(executor.submit(self._fetch_candlesticks, interval, symbol,
                                                      start), interval, symbol, start) for
                                     interval, symbol, start in timestamps]
                if timestamps:
                    with tqdm(total=len(timestamps), unit='saves', ncols=150, desc="Downloading Candlesticks") as pbar:
                        for future, interval, symbol, start in futures_to_params:
                            while future.running():
                                pass
                            new_candlesticks, interval, symbol = future.result()
                            candlesticks = connection.root.candlestick_collection[interval, symbol]
                            candlesticks.update(new_candlesticks)
                            pbar.update(1)
                            pbar.set_postfix(interval=interval, symbol=symbol, refresh=True)
                            connection.transaction_manager.commit()
            executor.shutdown(wait=True)

    def download_historical_trades(self):
        pass

    def download_aggregated_trades(self):
        pass

    def download_all_orders(self):
        pass

    def download_my_trades(self):
        pass

    def current_price_graph(self, assets=None):
        assets = set(assets)
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
            lambda x: (x['baseAsset'], x['quoteAsset'], prices[x['baseAsset'] + x['quoteAsset']]), trading_symbols
        ))
        inverse_edges = list(map(
            lambda x: (x['quoteAsset'], x['baseAsset'], 1 / prices[x['baseAsset'] + x['quoteAsset']]), trading_symbols
        ))
        edges.extend(inverse_edges)
        return utils.make_digraph(edges)

    def get_historical_candlesticks(self, interval, symbol, start=None, end=None):
        return self.service.candlesticks(symbol, interval, start=start, end=end).to_json(orient='records')

    def current_price(self, symbol=None):
        return self.service.ticker_price(symbol=symbol)
