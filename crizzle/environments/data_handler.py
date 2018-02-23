import logging
from abc import ABCMeta, abstractmethod
from crizzle.patterns.observer import Observer

logger = logging.getLogger(__name__)


class DataHandler(Observer, metaclass=ABCMeta):
    """
    Base class for all data handlers.
    Observer class that handles incoming updates to data grabbers.
    """

    @abstractmethod
    def handle(self, caller, state):
        """
        Handle data coming in from data grabber.

        Args:
            caller: The object emitting the event to be handled
            state: The new data associated with the event
        """
        pass
