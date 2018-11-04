import os
import json
import logging
from crizzle import services
from crizzle import feeds
from crizzle import utils

logger = logging.getLogger(__name__)


def get_default_data_directory():
    directory = os.path.join(os.path.expanduser('~'), 'crizzle')
    os.makedirs(directory, exist_ok=True)
    return directory


def set_data_directory(path):
    global data_dir
    os.makedirs(path, exist_ok=True)
    data_dir = path


set_service_key = services.set_key
get_service_key = services.get_key
get_service = services.get
get_feed = feeds.get
data_dir = get_default_data_directory()
