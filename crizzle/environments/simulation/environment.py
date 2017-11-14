from crizzle.environments import base
import logging

# TODO: implement empty methods

logger = logging.getLogger(__name__)


class Environment(base.Environment):
    """
    A sandbox environment for agents to train and test in using real data
    """
    _observation_space = base.Bounded(-1, 1)
    _action_space = base.Bounded(-1, 1)

    def __init__(self):
        super(Environment, self).__init__('simulation', None)
        self._positions = []
        self._info = {}
        self._observation = base.Observation()

    def add_agent(self, agent) -> None:
        super(Environment, self).add_agent(agent)

    @property
    def agents(self):
        return super(Environment, self).agents()

    @property
    def done(self):
        return super(Environment, self).done()

    @property
    def info(self) -> dict:
        return super(Environment, self).info

    @property
    def observation(self) -> base.Observation:
        return super(Environment, self).observation

    @property
    def observation_space(self) -> base.Space:
        return super(Environment, self).observation_space

    @property
    def action_space(self) -> base.Space:
        return __class__._action_space

    def render(self) -> None:
        pass

    def step(self, action: base.Action) -> base.Observation:
        pass

    def reset(self) -> base.Observation:
        pass

    def parse_returned(self, returned):
        pass

    def hashify(self, url=None, data=None):
        pass

    def query_private(self, url, data=None, params=None, headers=None):
        pass

    def query_public(self, url, data=None, params=None, headers=None):
        pass

    def query(self, url, data=None, params=None, headers=None, post=False):
        pass

    def get_positions(self) -> list:
        pass

    def get_current_rate(self, pair: str):
        pass

    def get_historical_data(self, pair: str, interval: int):
        pass


if __name__ == '__main__':
    # test singleton
    env = Environment()
    print(env.observation_space)
