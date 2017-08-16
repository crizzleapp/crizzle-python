class ParentAPI:
    def __init__(self, key_file=None):
        if key_file is not None:
            self.load_api_key(key_file)

    def load_api_key(self, key_file):
        with open(key_file, 'r') as f:
            lines = f.readlines()
            try:
                assert len(lines) == 2
                self.key, self.secret = lines
            except AssertionError as e:
                print('Key file must have key and secret on exactly two lines, instead has {}'.format(len(lines)))
                raise e

    def rate(self, target):
        pass
