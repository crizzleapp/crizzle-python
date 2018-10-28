import os
import logging
from abc import abstractmethod
from crizzle import services, feeds

logger = logging.getLogger(__name__)


class Feed:
    name = 'base'

    def __init__(self):
        logger.debug("Initialised new feed '{}'.".format(self.name))
        self.constants = self.service.constants

    @property
    def data_directory(self):
        return os.path.join(feeds.get_data_dir(), self.name)

    @property
    def service(self):
        return services.get(self.name)

    def initialize_cache(self):
        """
        Creates historical data file in the local data directory if it doesn't already exist.

        """
        os.makedirs(self.data_directory, exist_ok=True)

    @abstractmethod
    def update_cache(self):
        """
        Updates locally stored historical data.

        Returns:

        """
        pass
