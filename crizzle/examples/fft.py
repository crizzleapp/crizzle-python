import logging
import crizzle
import numpy as np

logging.basicConfig(format='%(asctime)s -- %(levelname)s: %(message)s',
                    handlers=[logging.StreamHandler()],
                    level=logging.DEBUG)

crizzle.set_data_directory('G:/Documents/CrizzleData')
env = crizzle.get_feed('binance')

a = env.candlesticks('EOSETH', env.constants.INTERVAL_1DAY)
