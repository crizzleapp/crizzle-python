import os
import ZODB as db
import atexit
from concurrent.futures import ThreadPoolExecutor
import crizzle
from crizzle import services, utils


class Feed:
    max_threads = 8

    def __init__(self, service_name, name=None):
        self.name = name or utils.misc.random_string()
        self.service_name = service_name
        self.logger = utils.log.get_logger('feed_{} ({})'.format(self.service_name, self.name))
        self.constants = self.service.constants
        self.time_multiplier = self.service.time_multiplier
        self.db = self.connect_database()
        self.logger.debug("Initialised feed with service '{}' ({}).".format(self.service_name, self.name))
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
        return os.path.join(crizzle.get_data_dir(), self.service_name + '.db')

    @property
    def service(self):
        return services.get(self.service_name)

    def connect_database(self):
        """
        Creates database file in the local data directory if it doesn't already exist.
        """
        self.logger.debug("Connecting to database '{}'...".format(self.database_path))
        database = db.DB(self.database_path,
                         pool_size=16,
                         database_name=self.name,
                         cache_size_bytes=409600,
                         cache_size=2)
        return database

    def reload_database(self):
        self.logger.debug("Reloading database '{}'...".format(self.database_path))
        self.db.close()
        self.db = self.connect_database()
