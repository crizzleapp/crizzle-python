import asyncio
import logging
import dataclasses
from . import runners
from . import receivers
from . import signals

logger = logging.getLogger('Crizzle')


@dataclasses.dataclass
class AppConfig:
    name: str = 'Crizzle'
    runner: runners.RunMode = runners.RunMode.RECORD
    logdir: str = '../logs'


class Application:
    """
    Top-level object.
    """

    def __init__(self, config: AppConfig):
        self.config = config
        self.name = self.config.name
        self.runner = self.config.runner.value(self.config)
        self.mode = runners.RunMode(self.config.runner).name
        self.setup()

    def setup(self):
        """
        Perform pre-run setup.

        Returns: None
        """
        signals.ready.send(self.__class__, instance=self)

    def run(self):
        """
        Run app.

        Returns: None
        """
        signals.pre_run.send(self.__class__, instance=self)
        asyncio.run(self.runner())
