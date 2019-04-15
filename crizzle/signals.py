"""
Defines the Event class and some common types of signals.
Loosely based on Django's Signals, with many advanced functions like caching and weakrefs removed.
"""

import logging
from threading import Lock

logger = logging.getLogger(__name__)


def make_id(target):
    if hasattr(target, '__func__'):
        return id(target.__self__), id(target.__func__)
    return id(target)


NONE_ID = make_id(None)


class Signal:
    def __init__(self, name, callback_args: list = None):
        self.callback_args = set(callback_args or [])
        self.name = name
        self._receivers = {}
        self.lock = Lock()

    def connect(self, receiver, sender=None, uid=None):
        if uid:
            lookup = (uid, make_id(sender))
        else:
            lookup = (make_id(receiver), make_id(sender))
        with self.lock:
            if lookup not in self._receivers:
                logger.info(f"Connected receiver {receiver} to event {self.name}")
                self._receivers[lookup] = receiver

    def disconnect(self, receiver=None, sender=None, uid=None):
        if uid:
            lookup = (uid, make_id(sender))
        else:
            lookup = (make_id(receiver), make_id(sender))
        disconnected = False
        with self.lock:
            to_delete = [key == lookup for key in self._receivers]
            for key in to_delete:
                disconnected = True
                del self._receivers[key]
                break
        return disconnected

    def has_receivers(self, *, sender=None) -> bool:
        return bool(self.receivers(sender=sender))

    def receivers(self, *, sender=None):
        receivers = []
        with self.lock:
            sender_key = make_id(sender)
            for (r_key, r_sender_key), receiver in self._receivers.items():
                if r_sender_key in (sender_key, NONE_ID):
                    receivers.append(receiver)
        return receivers

    def send(self, sender, **kwargs):
        for key in kwargs:
            if key not in self.callback_args:
                raise TypeError(f"Unexpected argument '{key}' for signal {self.name}")
        return [(receiver, receiver(sender=sender, **kwargs)) for receiver in self.receivers(sender=sender)]


def receiver(signal, sender=None, **kwargs):
    def _decorator(func):
        signals = signal if isinstance(signal, (list, tuple)) else [signal]
        for s in signals:
            s.connect(func, sender=sender, **kwargs)
        return func

    return _decorator


dummy = Signal('dummy')
ready = Signal('ready', callback_args=['instance'])
pre_run = Signal('pre_run', callback_args=['instance'])
order_placed = Signal('order_placed', callback_args=['instrument', 'type', 'side', 'rate'])
order_filled = Signal('order_filled', callback_args=['instrument', 'type', 'side', 'rate', 'outcome'])
