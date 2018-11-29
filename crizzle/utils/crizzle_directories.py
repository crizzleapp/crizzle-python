import os


class CrizzleDirectories:
    @staticmethod
    def get_default_crizzle_directory():
        directory = os.path.join(os.path.expanduser('~'), 'crizzle')
        os.makedirs(directory, exist_ok=True)
        return directory

    @staticmethod
    def get_crizzle_directory():
        return CrizzleDirectories._crizzle_dir

    @staticmethod
    def get_subdir(subdir_name):
        subdir_path = os.path.join(CrizzleDirectories._crizzle_dir, subdir_name)
        os.makedirs(subdir_path, exist_ok=True)
        return subdir_path

    @staticmethod
    def get_data_directory():
        return CrizzleDirectories.get_subdir('data')

    @staticmethod
    def get_log_directory():
        return CrizzleDirectories.get_subdir('logs')

    @staticmethod
    def set_data_directory(path):
        os.makedirs(path, exist_ok=True)
        CrizzleDirectories._crizzle_dir = path

    _crizzle_dir = get_default_crizzle_directory.__func__()
