Release: [![Build Status](https://travis-ci.org/tasercake/Crizzle.svg?branch=master)](https://travis-ci.org/tasercake/Crizzle) [![codecov](https://codecov.io/gh/tasercake/Crizzle/branch/master/graph/badge.svg)](https://codecov.io/gh/tasercake/Crizzle) Dev: [![Build Status](https://travis-ci.org/tasercake/Crizzle.svg?branch=dev)](https://travis-ci.org/tasercake/Crizzle)

# Crizzle

*A Python 3 algotrading library for cryptocurrency exchanges*

## About

Crizzle aims to be a simple algorithmic trading library for use by hobby traders, where the user is given access to both high- and low-level APIs for each exchange via `services` and `environments`.

As of 8-May-2018, Crizzle fully supports trading and data acquisition via the Binance API, and has partial (untested) support for the Poloniex API.

***Crizzle is still under development and should only be used for testing purposes.***

## Usage

```
git clone https://github.com/tasercake/Crizzle
```

```bash
pip install --editable .
```



Create an API key on your exchange (only Binance is supported at the moment).

Create a `binance.json` file at any location (Crizzle is strict about this file's name, so copy it as-is) to hold your API Key and Secret in the following format:

```json
{
	"key": "7sdfjshd7a109389df7g98strevb9dfds87",
	"secret": "fbs7896bdbs9842bs4s8n0ns00fn05nbdsf"
}
```



##### Option 1 - Services Only

With just the `<service_name>.json` file containing the API Key and Secret, it is possible to directly use Crizzle's `services` module -

````python
from crizzle import services
from crizzle import load_key

load_key("PATH_TO_KEY_FILE")  # Store key and secret as environment variables

binance = services.make('binance')
prices = binance.ticker_price()  # get the current price for every symbol on the exchange
candlesticks = binance.candlesticks()  # get historical OHLCV data
binance.order("TRXETH", "buy", "stop_limit", 500)  # place an order
````



##### Option 2 - Services and Environments

The usage of Crizzle's `envs` module requires one extra step of setup:

Create a `config.json` file at any location to hold your Crizzle configuration -

```json
{
  "data": "D:\\Crizzle\\data",  // Path to folder that holds data downloaded from services
  "keys": "D:\\Crizzle\\keys",  // Path to folder that contains API keys
}
```

Copy and save the following script as a `.py` file and run it.

```python
from crizzle import services, envs
from crizzle import load_config

load_config("PATH_TO_CONFIG_FILE")  # Stores contents of config file as environment variables

binance = services.make('binance')
prices = binance.ticker_price()  # get the current price for every symbol on the exchange
candlesticks = binance.candlesticks()  # get historical OHLCV data
binance.order("TRXETH", "buy", "stop_limit", 500)  # place an order

binance_env = envs.make('binance', symbols=["TRXETH", "EOSETH"], intervals=['4h', '1d'])
graph = binance_env.current_price_graph()
print(graph)
```

