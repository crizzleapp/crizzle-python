import functools


def memoize(f):
    """Memoize function f."""
    cache = f.cache = {}

    @functools.wraps(f)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]
    return memoizer
