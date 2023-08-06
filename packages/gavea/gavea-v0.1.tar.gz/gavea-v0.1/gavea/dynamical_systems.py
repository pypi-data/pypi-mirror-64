import numpy as np


class LinearTimeInvariantSystem(object):
    """ Linear time-invariant dynamical system """

    def __init__(self, y, A, B, C):
        # Save obervations
        self.y = y
        # Observation dimensions
        self.p, self.n = y.shape
        # State dimensions
        self.m = A.shape[0]
        # Control dimensions
        self.q = B.shape[1]
        # System matrix
        self.A = A
        # Input matrix
        self.B = B
        # Output matrix
        self.C = C

    def f(self, x, u, s, t):
        # State transition operator
        return self.A * x + self.B * u + s

    def h(self, x, e, o, t):
        # Measurement transition operator
        return self.C * x + e + o


class LinearTimeVaryingSystem(object):
    """ Linear time-varying dynamical system """

    def __init__(self, y, A, B, C):
        # Save obervations
        self.y = y
        # Observation dimensions
        self.p, self.n = y.shape
        # State dimensions
        self.m = list(A.values())[0].shape[0]
        # Control dimensions
        self.q = list(B.values())[0].shape[1]
        # System matrix
        self.A = A
        # Input matrix
        self.B = B
        # Output matrix
        self.C = C

    def f(self, x, u, s, t):
        # State transition operator
        return self.A[t] * x + self.B[t] * u + s

    def h(self, x, e, o, t):
        # Measurement transition operator
        return self.C[t] * x + e + o


class LinearRegression(LinearTimeVaryingSystem):
    """ Linear regression model """

    def __init__(self, y, X):
        # Save obervations
        self.y = y
        # Observation dimensions
        self.p, self.n = y.shape
        # State dimensions
        self.m = X.shape[0]
        # Control dimensions
        self.q = self.m
        # System matrix
        self.A = {t: 1.0 for t in range(self.n)}
        # Input matrix
        self.B = {t: 1.0 for t in range(self.n)}
        # Output matrix
        self.C = {t: X[:, t] for t in range(self.n)}


class LocalLevel(LinearTimeInvariantSystem):
    """ Local level dynamical system """

    def __init__(self, y):
        # Save obervations
        self.y = y
        # Observation dimensions
        self.p, self.n = y.shape
        # State dimensions
        self.m = self.p
        # Control dimensions
        self.q = self.p
        # System matrix
        self.A = 1.0
        # Input matrix
        self.B = 1.0
        # Output matrix
        self.C = 1.0


class LocalLinearTrend(LinearTimeInvariantSystem):
    """ Local linear trend dynamical system [local level + trend] """

    def __init__(self, y):
        # Save obervations
        self.y = y
        # Observation dimensions
        self.p, self.n = y.shape
        # State dimensions
        self.m = 2 * self.p
        # Control dimensions
        self.q = 2 * self.p
        # System matrix
        self.A = np.kron(np.identity(self.p), np.array(([1, 1], [0, 1])))
        # Input matrix
        self.B = np.identity(self.m)
        # Output matrix
        self.C = np.kron(np.identity(self.p), np.array([1, 0]))


class BasicStructuralModel(LinearTimeInvariantSystem):
    """ Structural model dynamical system [local level + seasonality]"""

    def __init__(self, y, s):
        # Save obervations
        self.y = y
        # Observation dimensions
        self.p, self.n = y.shape
        # State dimension
        self.m = self.p * (s + 1)
        # Control dimensions
        self.q = self.m
        # System matrix
        self.A = np.kron(
            np.identity(self.p),
            np.vstack(
                (
                    np.concatenate((np.array([1, 1]), np.zeros(s - 1)), axis=None),
                    np.concatenate((np.array([0, 1]), np.zeros(s - 1)), axis=None),
                    np.concatenate((np.array([0, 0]), -np.ones(s - 1)), axis=None),
                    np.concatenate(
                        (
                            np.zeros((s - 2, 2)),
                            np.identity(s - 2),
                            np.zeros((s - 2, 1)),
                        ),
                        axis=1,
                    ),
                )
            ),
        )
        # Input matrix
        self.B = np.identity(self.m)
        # Output matrix
        self.C = np.kron(
            np.identity(self.p), np.concatenate((np.array([1, 0, 1]), np.zeros(s - 2)))
        )


class MotionDynamics(LinearTimeInvariantSystem):
    """ Motion of a physical system as a function of time """

    def __init__(self, y, damping=0, delta=1):
        # Save obervations
        self.y = y
        # Observation dimensions
        self.p, self.n = y.shape
        # State dimension
        self.m = self.p * 2
        # Control dimensions
        self.q = self.p
        # System matrix
        self.A = np.kron(
            np.identity(self.p),
            np.array(
                ([1, (1 - damping * delta / 2) * delta], [0, (1 - damping * delta)])
            ),
        )
        # Input matrix
        self.B = np.kron(np.identity(self.p), np.array(([0.5 * delta ** 2], [delta])))
        # Output matrix
        self.C = np.kron(np.identity(self.p), np.array([1, 0]))
