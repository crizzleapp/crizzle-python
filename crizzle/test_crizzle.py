import os
import shutil
from . import set_data_directory, load_key


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
    path = 'tmp'
    os.makedirs(path, exist_ok=True)
    set_data_directory(path)
    assert os.environ['CrizzleData'] == '/datapath'
    assert os.environ['CrizzleKeys'] == '/keyspath'
    assert os.environ['CrizzleLog'] == '/logpath'
    shutil.rmtree(path)
