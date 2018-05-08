import os
import logging
from abc import abstractmethod
from crizzle import services
from crizzle import envs

logger = logging.getLogger(__name__)


class Feed(envs.DataGrabber):
    def __init__(self, name: str, key_file: str=None):
        super(Feed, self).__init__()
        self.name = name
        self.data_directory = envs.get_data_dir()
        self.service = services.make(self.name, key_file=key_file)
        # TODO: replace multiple files with a single file.
        logger.debug("Initialised new feed '{}'.".format(self.name))

    def initialize_file(self, filepath: str):
        """
        Creates historical data file in the local data directory if it doesn't already exist.

        Args:
            filepath (str): Full path to file

        Returns:
            None
        """
        if not os.path.isdir(self.data_directory):
            os.makedirs(self.data_directory)
        full_path = os.path.join(self.data_directory, filepath)
        if not os.path.exists(full_path):
            with open(full_path, 'w') as newfile:
                newfile.write('')

    @abstractmethod
    def update_local_historical_data(self):
        """
        Updates locally stored historical data.

        Returns:

        """
        pass

    @abstractmethod
    def next(self):
        pass
