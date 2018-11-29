import os
import json
import atexit
import logging
from crizzle import services
from crizzle import feeds
from crizzle import utils

logger = logging.getLogger(__name__)


get_log_dir = utils.CrizzleDirectories.get_log_directory
set_key = services.set_key
get_key = services.get_key
loaded_keys = services.loaded_keys
get_service = services.get
get_feed = feeds.get
set_crizzle_dir = utils.CrizzleDirectories.set_data_directory
get_crizzle_dir = utils.CrizzleDirectories.get_crizzle_directory
get_data_dir = utils.CrizzleDirectories.get_data_directory
