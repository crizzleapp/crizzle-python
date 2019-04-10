import os
from datetime import datetime
import asyncio
import logging
import dataclasses
from .runner import RunMode


@dataclasses.dataclass
class AppConfig:
    name: str = 'Crizzle'
    runner: RunMode = RunMode.RECORD
    logdir: str = '../logs'


class Application:
    def __init__(self, config: AppConfig):
        self.config = config
        self.name = self.config.name
        self.runner = self.config.runner.value(self.config)
        self.mode = RunMode(self.config.runner).name

    def setup_logging(self):
        root_logger = logging.getLogger('Crizzle')
        root_logger.setLevel(logging.DEBUG)
        logdir = self.config.logdir
        os.makedirs(logdir, exist_ok=True)
        log_file = os.path.join(logdir, f"log_{datetime.now().strftime('%Y%m%d_%H-%M-%S')}.txt")
        formatter = logging.Formatter("[%(asctime)s] [%(name)32s] [%(levelname)8s] -- %(message)s", '%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        root_logger.addHandler(stream_handler)
        root_logger.addHandler(file_handler)
        return root_logger

    def run(self):
        logger = self.setup_logging()
        logger.info(f"Starting App '{self.name}' in mode {self.mode}")
        asyncio.run(self.runner())
