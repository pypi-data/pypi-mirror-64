import cvxpy as cp
from .regularizers import ZeroRegularization


class StateSpaceModel(object):
    """
        Regularized State-Space models:

        min loss1(e) + loss2(u) + r1(o) + r2(s) + r3(x)
        s.t.
            x[t+1] = f(x[t], u[t], s[t])
            y[t] = h(x[t], e[t], o[t])

    """

    def __init__(
        self,
        y,
        system,
        gamma=0,
        rX=ZeroRegularization(),
        rO=ZeroRegularization(),
        rS=ZeroRegularization(),
    ):
        # Observed signal
        self.y = y
        # Number of observations
        self.n = y.shape[1]
        # Save system dynamics
        self.system = system
        # Save regularization
        self.rX, self.rO, self.rS = rX, rO, rS
        # Save loss miltiplicative coefficient
        self.gamma = gamma

    def filter(self):

        # Create decision variables
        # Measurement noise
        e = cp.Variable((self.system.p, self.n))
        # Measurement outliers
        o = cp.Variable((self.system.p, self.n))
        # State
        x = cp.Variable((self.system.m, self.n + 1))
        # Structural break
        s = cp.Variable((self.system.m, self.n))
        # Unobserved control
        u = cp.Variable((self.system.q, self.n))

        # Objective function
        obj = cp.Minimize(
            cp.sum_squares(e)
            + self.gamma * cp.sum_squares(u)
            + self.rX.expression(x)
            + self.rO.expression(o)
            + self.rS.expression(s)
        )

        #
        self.constraints = []
        for t in range(self.n):
            self.constraints.append(
                x[:, t + 1] == self.system.f(x[:, t], u[:, t], s[:, t], t)
            )
        for t in range(self.n):
            self.constraints.append(
                self.y[:, t] == self.system.h(x[:, t], e[:, t], o[:, t], t)
            )

        prob = cp.Problem(obj, self.constraints)
        self.result = prob.solve(verbose=True, solver=cp.OSQP)

        self.s = s.value
        self.e = e.value
        self.x = x.value
        self.o = o.value
        self.u = u.value
