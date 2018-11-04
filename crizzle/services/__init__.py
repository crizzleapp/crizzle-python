from crizzle.services import base
from crizzle.services import binance
from crizzle.utils import memoize


SERVICE_MAP = {'binance': binance,
               'poloniex': None,
               'kraken': None,
               'base': None}
SERVICES = list(SERVICE_MAP.keys())
KEYS = base.Keys
set_key = KEYS.set
get_key = KEYS.get


@memoize
def get(service_name: str, *args, **kwargs):
    service_name = service_name.lower()
    if service_name not in SERVICE_MAP:
        raise ValueError("Invalid Exchange Name '{}'.\n"
                         "Available Exchanges: {}".format(service_name, SERVICES))
    module = SERVICE_MAP[service_name]
    if module is not None:
        return module.Service(*args, **kwargs)

