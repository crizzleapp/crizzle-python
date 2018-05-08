import os
import json


def load_key(path):
    with open(path) as file:
        env_variable_name = 'CrizzleKey_{}'.format(os.path.splitext(os.path.split(path)[-1])[0])
        os.environ[env_variable_name] = file.read()


def load_config(path):
    with open(path, 'r') as file:
        config = json.load(file)
    os.environ['CrizzleData'] = config['data']
    os.environ['CrizzleLog'] = config['log']
    os.environ['CrizzleKeys'] = config['keys']
    for file_name in os.listdir(config['keys']):
        key_path = os.path.join(config['keys'], file_name)
        load_key(key_path)


if __name__ == '__main__':
    load_config('G:\\Documents\\Python Scripts\\crizzle\\config_example.json')
    print(os.environ['CrizzleKey_binance'])
