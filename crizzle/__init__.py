import os
import json
import logging

from crizzle import services
from crizzle import envs
from crizzle import patterns


logger = logging.getLogger(__name__)


def load_key(key, name=None):
    try:
        with open(key) as file:
            env_variable_name = 'CrizzleKey_{}'.format(os.path.splitext(os.path.split(key)[-1])[0])
            os.environ[env_variable_name] = file.read()
    except (FileNotFoundError, TypeError):
        try:
            assert name is not None
            env_variable_name = 'CrizzleKey_{}'.format(name)
            os.environ[env_variable_name] = key if isinstance(key, str) else json.dumps(key)
        except AssertionError:
            logger.error('Must provide service name if key is not a file path.')
        except json.JSONDecodeError:
            logger.error('Could not read contents of key.')


def load_config(path):
    with open(path, 'r') as file:
        config = json.load(file)
    os.environ['CrizzleData'] = config['data']
    os.environ['CrizzleLog'] = config['log']
    os.environ['CrizzleKeys'] = config['keys']
    for file_name in os.listdir(config['keys']):
        key_path = os.path.join(config['keys'], file_name)
        load_key(key_path)
