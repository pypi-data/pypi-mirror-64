"""Weight initialization schemes."""
import numpy as np


__all__ = [
    'Constant',
    'Normal',
    'Zeros'
]


class Initializer:
    """An initializer is used to set initial weights in a model."""

    def __str__(self):
        return self.__class__.__name__


class Constant(Initializer):
    """Constant initializer which always return the same value.

    Parameters:
        value (float): The constant value

    Example:

        ::

            >>> from creme import optim

            >>> init = optim.initializers.Constant(value=3.14)

            >>> init(shape=1)
            3.14

            >>> init(shape=2)
            array([3.14, 3.14])

    """

    def __init__(self, value):
        self.value = value

    def __call__(self, shape=1):
        return np.full(shape, self.value) if shape != 1 else self.value


class Zeros(Constant):
    """Initializer which return zeros for each new weight.

    Example:

        ::

            >>> from creme import optim

            >>> init = optim.initializers.Zeros()

            >>> init(shape=1)
            0.0

            >>> init(shape=2)
            array([0., 0.])

    """

    def __init__(self):
        super().__init__(value=0.)


class Normal(Initializer):
    """Random normal initializer which simulate a normal distribution with specified parameters.

    Parameters:
        mu (float): The mean of the normal distribution
        sigma (float): The standard deviation of the normal distribution

    Example:

        ::

            >>> from creme import optim

            >>> init = optim.initializers.Normal(mu=0, sigma=1, seed=42)

            >>> init(shape=1)
            0.496714

            >>> init(shape=2)
            array([-0.1382643 ,  0.64768854])

    """

    def __init__(self, mu=0., sigma=1., seed=None):
        self.mu = mu
        self.sigma = sigma
        self.seed = seed
        self._rng = np.random.RandomState(seed)

    def __call__(self, shape=1):
        weights = self._rng.normal(loc=self.mu, scale=self.sigma, size=shape)
        if shape == 1:
            return weights[0]
        return weights
