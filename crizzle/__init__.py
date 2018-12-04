from crizzle import services
from crizzle import feeds
from crizzle import utils

set_key = services.set_key
get_key = services.get_key
loaded_keys = services.loaded_keys
get_service = services.get
get_feed = feeds.get
logging = utils.log
register_callback = utils.dirs.register_callback
set_crizzle_dir = utils.dirs.set_data_directory
get_crizzle_dir = utils.dirs.get_crizzle_directory
get_data_dir = utils.dirs.get_data_directory
get_log_dir = utils.dirs.get_log_directory
