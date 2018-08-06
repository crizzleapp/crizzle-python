import os
import json
import logging

from crizzle import services
from crizzle import envs
from crizzle import patterns


logger = logging.getLogger(__name__)


def load_key(key, name=None):
    """
    Load contents of key to an environment variable.

    Args:
        key (Union[str, dict]): Path to a file containing the key in JSON format, OR a dict containing the key.
        name: Name of the service which the key belongs to.

    Returns:
        None
    """
    try:  # assume key is a file path (str)
        with open(key) as file:
            alt_name = os.path.splitext(os.path.split(key)[-1])[0]
            env_variable_name = 'CrizzleKey_{}'.format(alt_name)
            os.environ[env_variable_name] = file.read()
    except (FileNotFoundError, TypeError):  # if key is not a file path
        try:  # assume key is a dict
            assert name is not None
            env_variable_name = 'CrizzleKey_{}'.format(name)
            os.environ[env_variable_name] = json.dumps(key)
        except AssertionError:
            logger.error('Must provide service name if key is not a file path.')
        except json.JSONDecodeError:
            logger.error('Could not parse contents of key dict.')


def load_config(path):
    with open(path, 'r') as file:
        config = json.load(file)
    os.environ['CrizzleData'] = config['data']
    os.environ['CrizzleLog'] = config['log']
    os.environ['CrizzleKeys'] = config['keys']
    for file_name in os.listdir(config['keys']):
        key_path = os.path.join(config['keys'], file_name)
        load_key(key_path)
