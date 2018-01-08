class EnvironmentException(Exception):
    def __init__(self, message: str):
        super(EnvironmentException, self).__init__(message)