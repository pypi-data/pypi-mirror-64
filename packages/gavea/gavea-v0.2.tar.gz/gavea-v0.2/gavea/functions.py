import cvxpy as cp
from .util import UnknownParameter


class AtomicFunction(object):
    """ Abstract objective class """

    def __init__(self):
        return

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

    def __init__(self, coeff=UnknownParameter()):
        # Save multiplicative coefficient
        self.coeff = coeff

    def __str__(self):
        return "L1 norm objective function"

    def expression(self, u):
        return self.coeff * cp.sum(cp.abs(u))


class L2Norm(AtomicFunction):
    """ L2 norm (not squared), group-lasso regularization """

    def __init__(self, coeff=UnknownParameter()):
        # Save multiplicative coefficient
        self.coeff = coeff

    def __str__(self):
        return "L2 norm objective function"

    def expression(self, u):
        return self.coeff * sum(cp.norm(u[:, i], 2) for i in range(u.shape[1]))


class SumSquares(AtomicFunction):
    """
        Sum of squared entries given by:

        f(u; coeff) := coeff * sum(u[i]**2 for i in range(n))
    """

    def __init__(self, coeff=UnknownParameter()):
        # Save multiplicative coefficient
        self.coeff = coeff

    def __str__(self):
        return "Sum of squared entries objective function"

    def expression(self, u):
        return self.coeff * cp.sum_squares(u)


class QuadForm(AtomicFunction):
    """
        Quadratic form loss function given by:

        f(u; M) := u' * M * u
    """

    def __init__(self, M=UnknownParameter()):
        # Save quadratic form matrix
        self.M = M

    def __str__(self):
        return "Quadratic form loss function"

    def expression(self, u):
        return sum(cp.quad_form(u[:, i], self.M) for i in range(u.shape[1]))


class ZeroFunction(AtomicFunction):
    """ No objective function """

    def __str__(self):
        return "No objective function"

    def expression(self, u):
        return 0.0
