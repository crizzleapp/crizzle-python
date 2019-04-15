from enum import Enum
from abc import ABCMeta, abstractmethod


class Runner(metaclass=ABCMeta):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    async def __call__(self, *args, **kwargs):
        pass


class RecordRunner(Runner):
    async def __call__(self, *args, **kwargs):
        while True:
            pass


class TestRunner(Runner):
    async def __call__(self, *args, **kwargs):
        while True:
            pass


class LiveRunner(Runner):
    async def __call__(self, *args, **kwargs):
        while True:
            pass


class RunMode(Enum):
    RECORD = RecordRunner
    TEST = TestRunner
    LIVE = LiveRunner
