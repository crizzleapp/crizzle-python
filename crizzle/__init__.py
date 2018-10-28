import os
import json
import logging
from crizzle import services
from crizzle import feeds
from crizzle import utils

logger = logging.getLogger(__name__)
get_service = services.get
get_feed = feeds.get


def load_key(key_or_path, name=None):
    """
    Load contents of key to an environment variable.

    Args:
        key_or_path (Union[str, dict]): Path to a file containing the key in JSON format, OR a dict containing the key.
        name: Name of the service which the key belongs to.

    Returns:
        None
    """
    try:  # assume key is a file path (str)
        with open(key_or_path) as file:
            alt_name = os.path.splitext(os.path.split(key_or_path)[-1])[0]
            env_variable_name = 'CrizzleKey_{}'.format(alt_name)
            os.environ[env_variable_name] = file.read()
    except (FileNotFoundError, TypeError):  # if key is not a file path
        try:  # assume key is a dict
            assert name is not None
            env_variable_name = 'CrizzleKey_{}'.format(name)
            os.environ[env_variable_name] = json.dumps(key_or_path)
        except AssertionError:
            logger.error('Must provide service name if key is not a file path.')
        except json.JSONDecodeError:
            logger.error('Could not parse contents of key dict.')


def set_data_directory(path):
    if not os.path.isdir(path):
        raise NotADirectoryError("Invalid or missing directory for Crizzle data '{}'".format(path))
    os.environ['CrizzleData'] = os.path.join(path, 'data')
    os.makedirs(os.environ['CrizzleData'], exist_ok=True)
    os.environ['CrizzleLog'] = os.path.join(path, 'log')
    os.makedirs(os.environ['CrizzleLog'], exist_ok=True)
    os.environ['CrizzleKeys'] = os.path.join(path, 'keys')
    os.makedirs(os.environ['CrizzleKeys'], exist_ok=True)
    for key_file in os.listdir(os.environ['CrizzleKeys']):
        key_path = os.path.join(os.environ['CrizzleKeys'], key_file)
        load_key(key_path)
