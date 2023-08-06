import numpy as np
import cvxpy as cp


class AtomicFunction(object):
    """ Abstract objective class """

    def __init__(self, rho=1.0):
        # Save multiplicative coefficient
        self.rho = rho

    def __str__(self):
        return "Abstract objective function"

    def __add__(self, other):
        if isinstance(other, list):
            return other + [self]
        else:
            return [self, other]

    def __radd__(self, other):
        return self.__add__(other)

    def expression(self, u):
        return u

    def evaluate(self, u):
        return self.expression(u).value


class L1Norm(AtomicFunction):
    """ L1 norm, sum of absolute values """

    def __str__(self):
        return "L1 norm objective function"

    def expression(self, u):
        return self.rho * cp.sum(cp.abs(u))

    def prox(self, u, rho=1.0):
        t = self.rho / rho
        # soft-thresholding operator
        return np.maximum(u - t, 0.0) - np.maximum(-u - t, 0.0)


class L2Norm(AtomicFunction):
    """ L2 norm (not squared), group-lasso regularization """

    def __str__(self):
        return "L2 norm objective function"

    def expression(self, u):
        return self.rho * sum(cp.norm(u[:, i], 2) for i in range(u.shape[1]))

    def prox(self, u, rho=1.0):
        t = self.rho / rho

        # Block soft-thresholding operator
        _u = np.multiply(u, np.maximum(1.0 - np.divide(t, np.linalg.norm(u)), 0.0))
        _u[np.isnan(_u)] = 0.0

        return _u


class SumSquares(AtomicFunction):
    """ Sum of squared entries """

    def __str__(self):
        return "Sum of squared entries objective function"

    def compose(self, u, rho=1.0):
        t = self.rho / rho
        return u, (1.0 / (1.0 + t))

    def expression(self, u):
        return 0.5 * cp.sum_squares(u)

    def prox(self, u, rho=1.0):
        t = self.rho / rho
        return (1.0 / (1.0 + t)) * u


class ZeroRegularization(AtomicFunction):
    """ No objective function """

    def __str__(self):
        return "No objective function"

    def expression(self, u):
        return 0.0

    def prox(self, u, rho=1.0):
        return u
