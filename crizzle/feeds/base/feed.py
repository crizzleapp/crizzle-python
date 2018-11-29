import os
import logging
import ZODB as db
import atexit
from concurrent.futures import ThreadPoolExecutor
from abc import abstractmethod
from crizzle import services, utils

logger = logging.getLogger(__name__)
logging.getLogger("ZODB").setLevel(logging.WARNING)
logging.getLogger("txn").setLevel(logging.WARNING)


class Feed:
    max_threads = 8

    def __init__(self, service_name, name=None):
        self.name = name or utils.misc.random_string()
        self.service_name = service_name
        self.constants = self.service.constants
        self.time_multiplier = self.service.time_multiplier
        self.db = self.connect_database()
        logger.debug("Initialised new feed '{}' with service '{}'.".format(self.name, self.service_name))
        atexit.register(self.close)

    @property
    def time(self):
        return self.service.timestamp

    def close(self):
        self.db.close()

    def _threads(self):
        return ThreadPoolExecutor(max_workers=self.max_threads)

    @property
    def database_path(self):
        return os.path.join(utils.CrizzleDirectories.get_data_directory(), self.service_name + '.db')

    @property
    def service(self):
        return services.get(self.service_name)

    def connect_database(self):
        """
        Creates database file in the local data directory if it doesn't already exist.
        """
        logger.debug("Connecting to database '{}'...".format(self.database_path))
        database = db.DB(self.database_path,
                         pool_size=16,
                         database_name=self.name,
                         cache_size_bytes=409600,
                         cache_size=2)
        return database

    def reload_database(self):
        logger.debug("Reloading database '{}'...".format(self.database_path))
        self.db.close()
        self.db = self.connect_database()
