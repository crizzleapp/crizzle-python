[![Build Status](https://travis-ci.org/tasercake/Crizzle.svg?branch=master)](https://travis-ci.org/tasercake/Crizzle) [![Coverage Status](https://coveralls.io/repos/github/tasercake/Crizzle/badge.svg?branch=master)](https://coveralls.io/github/tasercake/Crizzle?branch=master)

# Crizzle

###### A Python 3 algotrading library for cryptocurrency exchanges

## About

Crizzle aims to be a simple algorithmic trading library for use by hobby traders, where the user is given access to both high- and low-level APIs for each exchange via `services` and `environments`.

As of 05/05/2018, Crizzle fully supports trading and data acquisition via the Binance API, and has partial (untested) support for the Poloniex API.

## Usage

```
git clone https://github.com/tasercake/Crizzle
```

```bash
pip install --editable .
```

Create an API key on your exchange (only Binance is supported at the moment).

Create a `.txt` file that contains your API Key and Secret on exactly 2 lines like so:

```
7sdfjshd7a109389df7g98strevb9dfds87  # Key
fbs7896bdbs9842bs4s8n0ns00fn05nbdsf  # Secret
```

Copy and save the following script as a `.py` file and run it.

```python
from crizzle import services
from crizzle import envs

KEY_PATH = "PATH_TO_KEY_FILE"

binance = services.make('binance', key_file=KEY_PATH)
prices = binance.ticker_price()
candlesticks = binance.candlesticks()
binance.order("TRXETH", "buy", "stop_limit", 500)

binance_env = envs.make('binance', key_file=KEY_PATH, symbols=["TRXETH", "EOSETH"], intervals=['4h', '1d'])
graph = binance_env.current_price_graph()
print(graph)
```

