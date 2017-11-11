import json
import logging
from app.data_handlers import RateDataHandler
from app.environments import simulation
from app.agent import Agent

# region Read Config
with open('config.json') as file:
    config = json.load(file)
    pairs = config['pairs']
    exchanges = config['exchanges']
    data_location = config['data_location']
    valid_intervals = config['valid_intervals']
# endregion


# region Environments
env = simulation.Environment()
# endregion


# region Data Handler
historical = RateDataHandler(data_dir=data_location, exchange=simulation.Environment())
# endregion


# region Agent
agent = Agent()
# endregion
