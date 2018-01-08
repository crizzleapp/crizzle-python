"""
A set of parent classes to implement the Observer design pattern.
These are used to enable the  event-driven nature of crizzle.
"""
import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


class Observable:
    """
    A parent class for objects that update themselves or put out notifications

    Examples
        Register an observer, update the object's state, and all registered observer
        will handle the update appropriately.

        Data handlers - On the arrival of new data, update the object's state so observers know when to emit an event.
    """
    def __init__(self):
        self._observers = set()
        self._state = None

    def register(self, observer):
        self._observers.add(observer)
        observer.add_subject(self)

    def unregister(self, observer):
        self._observers.remove(observer)

    def _notify(self):
        for observer in self._observers:
            observer.handle(self, )

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state
        self._notify()


class Observer(metaclass=ABCMeta):
    """
    A parent class for objects that receive update events from its subjects
    """
    def __init__(self):
        self._subjects = set()

    @abstractmethod
    def handle(self, caller, state):
        """
        Method to be overridden to handle the state update appropriately

        Args:
            caller: the instance that calls this method
            state: the new state of the calling instance

        Returns:
            None
        """
        pass

    @abstractmethod
    def can_handle(self, caller, state) -> bool:
        pass

    @property
    def subjects(self):
        return self.subjects

    def add_subject(self, subject):
        assert isinstance(subject, Observable)
        self._subjects.add(subject)


class HandlerChain(Observer):
    """
    Implementation of the Chain of Responsiblity pattern.
    """
    def __init__(self):
        super(HandlerChain, self).__init__()
        self._handlers = []

    def add_handler(self, handler):
        assert isinstance(handler, Observer)
        self._handlers.append(handler)

    def remove_handler(self, handler):
        if handler in self._handlers:
            self._handlers.remove(handler)

    def handle(self, caller, state):
        handled = False
        if len(self._handlers) == 0:
            raise Exception("Handler chain is empty.")
        for handler in self._handlers:
            if handler.can_handle(caller, state):
                handler.handle(caller, )
                handled = True
        if not handled:
            raise Exception("No valid handlers found.")

    def can_handle(self, caller, state):
        return True


if __name__ == '__main__':
    class ConcreteObserver1(Observer):
        def can_handle(self, caller, state) -> bool:
            return isinstance(state, int)

        def handle(self, caller, state):
            print("called by {}, new state: {}, handled by 1".format(caller, state))


    class ConcreteObserver2(Observer):
        def can_handle(self, caller, state) -> bool:
            return isinstance(state, str)

        def handle(self, caller, state):
            print("called by {}, new state: {}, handled by 2".format(caller, state))


    sub = Observable()
    chain = HandlerChain()
    obs1 = ConcreteObserver1()
    obs2 = ConcreteObserver2()
    sub.register(chain)
    chain.add_handler(obs1)
    chain.add_handler(obs2)
    sub.state = "test 1"
    sub.state = 2
