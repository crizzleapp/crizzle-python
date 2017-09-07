import tensorflow as tf
import pandas as pd
import numpy as np
import random
import read_historical as rh
pd.set_option('display.width', 300)

# region HYPERPARAMETERS
BATCH_SIZE = 10
# endregion


# region GENERATE TRAINING DATA
# endregion


if __name__ == '__main__':
    data = rh.load_historical_data('USDT_BTC', 15)
    print(rh.select(data, rh.DESIRED_COLUMNS, 0, BATCH_SIZE))