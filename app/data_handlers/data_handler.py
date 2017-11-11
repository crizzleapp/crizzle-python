import logging
import time
import environments
import pandas as pd
from singleton import Singleton

logger = logging.getLogger(__name__)


class DataHandler(metaclass=Singleton):
    """
    Base class for all data handlers.
    """

    def __init__(self):
        pass

    def get_data(self):
        raise NotImplementedError()

    def update_all(self):
        """
        Update all loaded data
        :return:
        """
        raise NotImplementedError()