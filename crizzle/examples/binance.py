import crizzle

crizzle.logging.set_min_log_level(2)
crizzle.set_crizzle_dir('G:/Documents/CrizzleData')
crizzle.set_key('binance', "G:/Documents/CrizzleData/keys/binance_test.json")
feed = crizzle.get_feed('binance')
feed.download_candlesticks(min_interval_seconds=300, symbols=['EOSETH'])
