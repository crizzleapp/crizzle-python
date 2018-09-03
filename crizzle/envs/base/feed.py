import os
import logging
from abc import abstractmethod
from crizzle import services
from crizzle import envs

logger = logging.getLogger(__name__)


class Feed:
    def __init__(self, name: str):
        super(Feed, self).__init__()
        self.name = name
        self.data_directory = os.path.join(envs.get_data_dir(), self.name)
        self.service = services.get(self.name)
        logger.debug("Initialised new feed '{}'.".format(self.name))

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
