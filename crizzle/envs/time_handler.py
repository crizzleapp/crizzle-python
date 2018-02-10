from datetime import datetime, timezone

# UNIX time constants
MINUTE = 60
HOUR = 60 * 60
DAY = 60 * 60 * 24
WEEK = DAY * 7
MONTH = DAY * 30
YEAR = DAY * 365


def check_valid_time_period(num_seconds):
    if num_seconds not in [300, 900, 1800, 7200, 14400, 86400]:
        raise Exception("""Invalid time period {}. valid time periods are:
                               \n[300, 900, 1800, 7200, 14400, 86400]""".format(num_seconds))


def current_time(as_unix=True):
    dt = datetime.utcnow()
    if as_unix:
        return dt.timestamp()
    return dt


# noinspection SpellCheckingInspection,SpellCheckingInspection
def to_unix(*args, **kwargs):
    """
    Return the UNIX timestamp representation of the given UTC date and time
    :return:
    """
    if 'tzinfo' not in kwargs:
        kwargs['tzinfo'] = timezone.utc
    dt = datetime(*args, **kwargs)
    return dt.timestamp()


def to_utc(timestamp, as_str=True):
    """
    Convert a given UNIX timestamp to date and time in UTC
    If as_str is true, returns full string representation, else returns datetime object
    :param timestamp: floating point value of the UNIX timestamp to convert to UTC
    :type timestamp: float
    :param as_str: whether or not to return string representation instead of datetime object
    :type as_str: bool
    :return:
    """
    dt = datetime.utcfromtimestamp(timestamp)
    if as_str:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt


# For any * imports
__all__ = ['MINUTE', 'HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR', 'to_unix', 'to_utc', 'current_time']


if __name__ == '__main__':
    print(to_utc(to_unix(2015, 1, 1, tzinfo=timezone.utc)))
