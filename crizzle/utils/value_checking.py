def assert_not_none(obj, name):
    """
    Raise ValueError if obj is None.

    Args:
        obj: object to check
        name: name of object (to be included in exception message)

    Raises:
        ValueError
    """
    if obj is None:
        raise ValueError("'{}' cannot be None.".format(name))


def assert_none(obj, name):
    """
    Raise ValueError if obj is not None.

    Args:
        obj: object to check
        name: name of object (to be included in exception message)

    Raises:
        ValueError
    """
    if obj is not None:
        raise ValueError("'{}' must be None.".format(name))


def assert_in(obj, name, space):
    """
    Raise ValueError if obj is not contained in space.

    Args:
        obj: object to check
        name: name of object (to be included in exception message)
        space: iterable to check for object in

    Raises:
        ValueError
    """
    if obj not in space:
        raise ValueError("'{}' must be in '{}', got '{}' instead.".format(name, space, obj))


def assert_equal(obj, name, expected_value):
    """
    Raise ValueError if obj does not equal expected_value

    Args:
        obj: object to check
        name: name of object (to be included in exception message)
        expected_value: expected value to check against

    Raises:
        ValueError
    """
    if obj != expected_value:
        raise ValueError("'{}' must have value '{}', got '{}' instead.".format(name, expected_value, obj))


def assert_type(obj, name, expected_type):
    """
    Raise TypeError if obj is not of the expected type

    Args:
        obj: object to check
        name: name of object (to be included in exception message)
        expected_type: type to check obj against

    Raises:
        TypeError
    """
    if not isinstance(obj, expected_type):
        raise TypeError("'{}' must be of type '{}', got '{}' instead.".format(name, expected_type, type(obj)))
