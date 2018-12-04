import logging
from crizzle.utils import crizzle_dirs
import tqdm
import datetime
import os
import sys

MAX_LOGS = 10
MAX_LOG_AGE = 3600 * 24 * 30


# logging.getLogger("urllib3").setLevel(logging.WARNING)
# logging.getLogger("ZODB").setLevel(logging.WARNING)
# logging.getLogger("txn").setLevel(logging.WARNING)


class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super(self.__class__, self).__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg, file=sys.stderr)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


def get_root_logger():
    logger = logging.getLogger()
    _set_console_handler(logger)
    _set_file_handler(logger)
    return logger


def _set_console_handler(logger, level=logging.INFO):
    stream_formatter = logging.Formatter('[%(asctime)s] [%(levelname)-8s] -- %(message)s', "%Y-%m-%d %H:%M:%S")
    stream_handler = TqdmLoggingHandler(level=level)
    stream_handler.setFormatter(stream_formatter)
    stream_handler.setLevel(level)
    logger.addHandler(stream_handler)
    return stream_handler


def _set_file_handler(logger, level=logging.DEBUG):
    # File logging
    file_formatter = logging.Formatter('[%(asctime)s] [%(name)-30.30s] [%(levelname)-8s]'
                                       ' -- %(message)s', "%Y-%m-%d %H:%M:%S")
    print(_get_log_file())
    file_handler = logging.FileHandler(_get_log_file())
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)
    return file_handler


def _get_log_file():
    _clean_log_dir()
    log_dir = crizzle_dirs.dirs.get_log_directory()
    name = '{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    path = os.path.join(log_dir, name)
    return path


def _clean_log_dir():
    pass


def set_min_log_level(level):
    root_logger.setLevel(level)
    for handler in root_logger.handlers[:]:
        handler.setLevel(level)


def set_verbosity(level):
    assert isinstance(level, int)
    set_min_log_level(max(0, 5 - level))


def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger('crizzle.{}'.format(name))
    if level is not None:
        logger.setLevel(level)
    return logger


root_logger = get_root_logger()
crizzle_dirs.dirs.register_callback(_set_file_handler, root_logger)
