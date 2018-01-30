"""
Base class for all remote exchange data grabbers
"""

import logging
from abc import ABCMeta, abstractmethod
from crizzle.data.data_grabber import DataGrabber

logger = logging.getLogger(__name__)


class ExchangeDataGrabber(DataGrabber, metaclass=ABCMeta):
    def __init__(self, root=None):
        super(ExchangeDataGrabber, self).__init__()
        self.source = root
        self._subscribe()

    @abstractmethod
    def _subscribe(self):
        """
        Subscribe to the remote exchange's ticker if available.

        Returns:
            None
        """
        pass
