import os
import logging
from abc import abstractmethod
from crizzle import services
from crizzle import environments

logger = logging.getLogger(__name__)


class Feed(environments.DataGrabber):
    def __init__(self, name: str, key_file: str=None):
        super(Feed, self).__init__()
        self.name = name
        self.data_directory = os.path.join(environments.get_local_data_dir(), self.name)
        self.service = services.make(self.name, key_file=key_file)
        # TODO: determine if dynamic file creation is necessary in the general case
        # TODO: if so, replace pre-emptive file creation with dynamic file creation
        logger.debug("Initialised new feed '{}'.".format(self.name))

    def create_nonexistent_files(self, files: dict):
        """
        Creates non-existent files in the local data directory.

        Args:
            files (dict): Dictionary of the format {folder1: [files...], folder2: [files...]}

        Returns:
            None
        """
        if not os.path.isdir(self.data_directory):
            os.makedirs(self.data_directory)
        for folder in files.keys():
            folder_path = os.path.join(self.data_directory, folder)
            if not os.path.isdir(folder_path):
                os.makedirs(folder_path)
            for file in files[folder]:
                full_path = os.path.join(self.data_directory, folder, file)
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

    def __str__(self):
        return "Feed instance '{}' ({})".format(self.name, 'not authenticated' if self.service.api_key is None else 'authenticated')


if __name__ == '__main__':
    class ConcreteFeed(Feed):
        def update_local_historical_data(self, symbol: str, data_type: str):
            pass

        def next(self):
            pass

    key = 'G:\\Documents\\Python Scripts\\crizzle\\data\\keys\\binance_test.apikey'
    data_dir = 'G:\\Documents\\Python Scripts\\crizzle\\data\\historical'
    feed1 = ConcreteFeed('binance', key_file=key)
    feed2 = ConcreteFeed('binance', key_file=key)
    print(feed1.service is feed2.service)  # Check singleton
    print(feed1.data_directory)  # Verify data directory
