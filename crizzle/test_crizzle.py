import os

from . import load_config, load_key


def test_load_key():
    path = 'tmp.json'
    data = '{"key": "key", "secret": "secret"}'
    with open(path, 'w') as tmp:
        tmp.write(data)
    load_key(path)
    assert os.environ['CrizzleKey_tmp'] is not None
    assert os.environ['CrizzleKey_tmp'] == data
    os.remove(path)


def test_load_config():
    path = 'tmp.json'
    data = '{"data": "/datapath", "keys": "/keyspath", "log": "/logpath"}'
    with open(path, 'w') as tmp:
        tmp.write(data)
    try:
        load_config(path)
    except FileNotFoundError:
        pass
    assert os.environ['CrizzleData'] == '/datapath'
    assert os.environ['CrizzleKeys'] == '/keyspath'
    assert os.environ['CrizzleLog'] == '/logpath'
    os.remove(path)
