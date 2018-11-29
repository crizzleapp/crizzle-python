import logging
import crizzle

logging.basicConfig(format='%(asctime)s -- %(levelname)s: %(message)s', handlers=[logging.StreamHandler()],
                    level=logging.DEBUG)

crizzle.set_crizzle_dir('G:/Documents/CrizzleData')
crizzle.set_key('binance', "G:/Documents/CrizzleData/keys/binance_test.json")
feed = crizzle.get_feed('binance')
# print(feed._match_symbols(['ETH.*', 'EOS.*', 'TRX.*', 'BTC.*']))
feed.download_candlesticks(min_interval_seconds=300000, symbols=['EOSETH'])
# print(feed.get_update_timestamps(min_interval_seconds=30000))
