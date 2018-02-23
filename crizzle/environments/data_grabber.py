import logging
from abc import ABCMeta, abstractmethod
from crizzle.patterns.observer import Observable

logger = logging.getLogger(__name__)


class DataGrabber(Observable, metaclass=ABCMeta):
    """
    Base class for all objects that grab data from a remote or local source and emit events.
    """
    @abstractmethod
    def next(self):
        return False
