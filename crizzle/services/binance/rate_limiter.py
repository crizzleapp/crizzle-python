"""
API call-rate limiter for the Binance service.
Currently unused.
"""

import time
import json


class RateLimiter:
    DEFAULT_LIMITS = {
        "requests": {"minute": 1200},
        "order": {"second": 10, "day": 100000}
    }

    def __init__(self):
        self._limits = RateLimiter.DEFAULT_LIMITS
        self._order_quota = 0
        self._request_quota = 0

    @property
    def limits(self):
        return self._limits

    def set_limits(self, limits):
        if isinstance(limits, str):
            limits = json.loads(limits)
        limits_dict = {}
        for limit in limits:
            limit_type = limit['rateLimitType'].lower()
            limit_interval = limit['interval'].lower()
            limit_quantity = int(limit['limit'])
            if limit_type not in limits_dict:
                limits_dict[limit_type] = {}
            limits_dict[limit_type][limit_interval] = limit_quantity
        self._limits = limits_dict

    def calulate_weight(self, endpoint, *args, **kwargs):
        pass


if __name__ == '__main__':
    limiter = RateLimiter()
    limiter.set_limits([
        {
            "rateLimitType": "REQUESTS_WEIGHT",
            "interval": "MINUTE",
            "limit": 1200
        },
        {
            "rateLimitType": "ORDERS",
            "interval": "SECOND",
            "limit": 10
        },
        {
            "rateLimitType": "ORDERS",
            "interval": "DAY",
            "limit": 100
        }
    ])
    print(limiter.limits)
