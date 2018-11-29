from persistent import mapping, Persistent
from BTrees import LOBTree, OOBTree


class Candlestick(mapping.PersistentMapping):
    def __init__(self,
                 timestamp,
                 open_price,
                 high_price,
                 low_price,
                 close_price,
                 volume=None,
                 quote_volume=None,
                 close_timestamp=None,
                 **kwargs):
        super(Candlestick, self).__init__()
        self.update({'timestamp': timestamp,
                     'open_price': open_price,
                     'high_price': high_price,
                     'low_price': low_price,
                     'close_price': close_price,
                     'volume': volume,
                     'quote_volume': quote_volume,
                     'close_timestmap': close_timestamp
                     })
        self.update(kwargs)

    @property
    def timestamp(self):
        return self['timestamp']

    @property
    def open_price(self):
        return self['open_price']

    @property
    def high_price(self):
        return self['high_price']

    @property
    def low_price(self):
        return self['low_price']

    @property
    def close_price(self):
        return self['close_price']

    @property
    def volume(self):
        return self['volume']

    @property
    def quote_volume(self):
        return self['quote_volume']

    @property
    def close_timestamp(self):
        return self['close_timestmap']


class Candlesticks(LOBTree.BTree):
    def most_recent(self):
        if not len(self):
            return 0
        else:
            return self.maxKey()


class CandlestickCollection(OOBTree.BTree):
    pass
