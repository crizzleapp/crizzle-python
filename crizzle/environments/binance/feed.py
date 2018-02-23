from crizzle.environments.base import Feed as BaseFeed
from crizzle.patterns.directory import Directory


class Feed(BaseFeed):
    def __init__(self, local_dir: str, symbols: list=None,  key_file: str=None):
        self.symbols = symbols
        super(Feed, self).__init__('binance', key_file=key_file)
        self.all_symbols = self.service.trading_symbols()
        self.files = {'candlestick': ['1d.csv', '4h.csv', '1h.csv'], 'trades': ['trades.csv']}

    def get_folder_structure(self, symbols: list, intervals: list):
        output = Directory('candlestick')
        for symbol in symbols:
            for interval in intervals:
                output.add_file()

    def check_local_data(self) -> dict:
        """
        Checks local data directory for file existence and most recent datapoint for each data type+

        Returns:

        """
        pass

    def get_historical_trades(self, symbol, start=None, end=None, from_id=None):
        if start is not None and end is not None:
            assert from_id is None

    def get_historical_candlesticks(self, symbol, interval, start=None, end=None):
        pass

    def update_local_historical_data(self, symbol: str, data_type: str):
        assert data_type in ('candlesticks', 'trades')

        if data_type == 'candlesticks':
            pass
        elif data_type == 'trades':
            pass

    def next(self):
        pass


if __name__ == '__main__':
    key = 'G:\\Documents\\Python Scripts\\crizzle\\data\\keys\\binance.apikey'
    feed = Feed('G:\\Documents\\Python Scripts\\crizzle\\data\\historical\\Binance', symbols=['EOSETH'], key_file=key)
    print(feed.all_symbols)
