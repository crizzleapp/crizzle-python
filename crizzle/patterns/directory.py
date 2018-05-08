import os
import json


class Directory():
    def __init__(self, name=None, source=None):
        self.name = name
        self.subdirectories = dict()
        self.files = set()
        if source is not None:
            if isinstance(source, str):
                with open(source, 'r') as file:
                    source = json.load(file)
            self.load_from_list(source)

    @property
    def has_files(self):
        return len(self.files) != 0

    def add_file(self, name):
        self.files.add(name)

    def add_subdirectory(self, name):
        new_directory = Directory(name)
        self.subdirectories[name] = new_directory
        return new_directory

    @property
    def has_subdirectories(self):
        return len(self.subdirectories) != 0

    def load_from_list(self, source: list):
        """
        Load directory tree from a recursive list of the format [dirname, [files...], [subdirs...]]

        Args:
            source: recursive list of the format [dirname, [files...], [subdirs...]]

        Returns:
            None
        """
        for directory in source:
            new_dir = self.add_subdirectory(directory[0])  # add directories to self.subdirectories
            for file in directory[1]:
                new_dir.add_file(file)  # add files to self.files
            if self.has_subdirectories:
                self.load_directory(directory[2], self.subdirectories[new_dir.name])

    def load_directory(self, source, parent):
        for directory in source:
            new_dir = parent.add_subdirectory(directory[0])
            for file in directory[1]:
                new_dir.add_file(file)
            if parent.has_subdirectories:
                self.load_directory(directory[2], parent.subdirectories[new_dir.name])

    def listify(self):
        output = [self.name, list(self.files), []]
        for key, value in self.subdirectories.items():
            output[2].append(key)
            output[2].append(value.listify())
        return output

    def as_list(self):
        return self.listify()[2:]

    def as_dict(self):
        output = {self.name: {'files': list(self.files), 'subdirectories': []}}
        for key, value in self.subdirectories.items():
            output[self.name]['subdirectories'].append(value.as_dict())
        return output

    def __str__(self):
        return "Directory '{}': {}".format(self.name, self.as_list().__str__())

    def __eq__(self, other):
        return self.subdirectories == other.subdirectories and self.files == other.files
