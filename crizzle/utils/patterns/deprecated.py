import warnings
from functools import wraps


def deprecated(message):
    """
    A decorator to mark functions as deprecated.

    Args:
        message: Deprecation message.
    """

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn("Function {} has been deprecated. {}".format(func.__name__, message),
                          category=DeprecationWarning,
                          stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)

        return wrapped

    return decorator
