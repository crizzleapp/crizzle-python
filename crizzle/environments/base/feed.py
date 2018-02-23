import os
from abc import abstractmethod
from crizzle import services
from crizzle import environments


class Feed(environments.DataGrabber):
    def __init__(self, name: str, files: dict=None, key_file: str=None):
        super(Feed, self).__init__()
        self.name = name
        self.dir = os.path.join(environments.get_local_data_dir(), self.name)
        self.service = services.make(self.name, key_file=key_file)
        if files is not None:
            self.create_nonexistent_files(files=files)

    def create_nonexistent_files(self, files: dict):
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir)
        for folder in files.keys():
            folder_path = os.path.join(self.dir, folder)
            if not os.path.isdir(folder_path):
                os.makedirs(folder_path)
            for file in files[folder]:
                full_path = os.path.join(self.dir, folder, file)
                if not os.path.exists(full_path):
                    with open(full_path, 'w') as newfile:
                        newfile.write('')

    @abstractmethod
    def update_local_historical_data(self, symbol: str, data_type: str):
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
    feed1 = ConcreteFeed('binance', files={}, key_file=key)
    feed2 = ConcreteFeed('binance', files={}, key_file=key)
    print(feed1.service is feed2.service)  # Check singleton
    print(feed1.dir)  # Verify data directory
