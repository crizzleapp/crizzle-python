import os


class _CrizzleDirs:
    def __init__(self, **kwargs):
        super(_CrizzleDirs, self).__init__(**kwargs)
        self.is_default = True
        self._crizzle_dir = self.set_data_directory(self.get_default_crizzle_directory())
        self._callbacks = []

    def register_callback(self, func, *args, **kwargs):
        self._callbacks.append((func, args, kwargs))

    def run_callbacks(self):
        for callback, args, kwargs in self._callbacks:
            callback(*args, **kwargs)

    def get_default_crizzle_directory(self):
        directory = os.path.join(os.path.expanduser('~'), '.crizzle')
        os.makedirs(directory, exist_ok=True)
        return directory

    def get_crizzle_directory(self):
        return self._crizzle_dir

    def get_subdir(self, subdir_name):
        subdir_path = os.path.join(self._crizzle_dir, subdir_name)
        os.makedirs(subdir_path, exist_ok=True)
        return subdir_path

    def get_data_directory(self):
        return self.get_subdir('data')

    def get_log_directory(self):
        return self.get_subdir('log')

    def set_data_directory(self, path):
        os.makedirs(path, exist_ok=True)
        self._crizzle_dir = path
        if not self.is_default:
            self.run_callbacks()
        self.is_default = False
        return path


dirs = _CrizzleDirs()
