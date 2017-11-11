import os
import json
import logging
import datetime
import environments
import data_handlers
import agent

# region Read Config
with open('config.json') as config_file:
    config = json.load(config_file)
    pairs = config['pairs']
    exchanges = config['exchanges']
    project_directory = config['project_directory']
    historical_exchange = config['historical_exchange']
    num_logs = config['num_logs']
# endregion


# region Logging setup
log_directory = project_directory + "\\data\\log"
existing_logs = sorted([filename for filename in os.listdir(log_directory) if filename.endswith('.txt')])

while len(existing_logs) >= num_logs:
    os.remove(log_directory + "\\" + existing_logs[0])
    existing_logs = sorted([filename for filename in os.listdir(log_directory) if filename.endswith('.txt')])

log_path = log_directory + "\\{}.txt".format(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
log_handlers = [logging.FileHandler(log_path), logging.StreamHandler()]
logging.basicConfig(level=logging.DEBUG, format=log_format, handlers=log_handlers)
# endregion


# region Environments
env = environments.simulation.Environment()
# endregion


# region Data Handler
historical = data_handlers.RateDataHandler(data_dir=project_directory + "\\data\\historical",
                                           exchange=environments.get_environment(historical_exchange))
# endregion


# region Agent
bot = agent.Agent()
# endregion
