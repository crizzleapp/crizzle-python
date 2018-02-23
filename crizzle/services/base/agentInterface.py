from random import uniform, choice


class Observation:
    def __init__(self):
        pass


class Action:
    def __init__(self):
        pass


class Space:
    def sample(self):
        pass


class Bounded(Space):
    def __init__(self, low: (float, list), high: (float, list)):
        if isinstance(low, float):
            assert isinstance(high, float)
            self._shape = 1
        elif isinstance(low, list):
            assert isinstance(high, list)
            assert len(low) == len(high)
            for lower, higher in zip(low, high):
                assert lower <= higher
            self._shape = len(low)
        self._low = low
        self._high = high

    @property
    def low(self):
        return self._low

    @property
    def high(self):
        return self._high

    @property
    def shape(self) -> int:
        """
        Dimensionality of box.
        Not the same as numpy shape.

        Returns:
            Dimensionality of the box
        """
        return self._shape

    def sample(self) -> (float, list):
        if isinstance(self._low, float):
            return uniform(self._low, self._high)
        else:
            return [uniform(low, high) for low, high in zip(self._low, self._high)]

    def contains(self, x):
        if len(x) == self._shape:
            lowerbounded = all([item >= bound for item, bound in zip(x, self._low)])
            upperbounded = all([item <= bound for item, bound in zip(x, self._high)])
            return lowerbounded and upperbounded
        return False


class Discrete(Space):
    def __init__(self, n: list):
        self.n = n

    def sample(self):
        return choice(self.n)

    def contains(self, x):
        return x in self.n


if __name__ == '__main__':
    # box = Bounded([-10, 2, 9], [-9, 3, 10])
    # print(box.contains([-9, 2, 9]))
    # print(box.sample())
    # print(box.contains([-11, 2, 9]))

    disc = Discrete([1, 2, 3, 4, 5])
    print(disc.sample())
